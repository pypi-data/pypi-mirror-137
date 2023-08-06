import os
import logging

from PIL import Image

from google.api_core.exceptions import NotFound
from google.cloud import artifactregistry_v1beta2
from google.cloud.artifactregistry_v1beta2 import CreateRepositoryRequest, Repository
from google.cloud.devtools import cloudbuild_v1
from google.cloud import storage as google_storage
import google.auth
from google.auth import compute_engine
from google.cloud.devtools.cloudbuild_v1 import Source, StorageSource

from label_studio_tools.core.utils.params import get_env
from label_studio_tools.core.utils.io import get_local_path

DATA_UNDEFINED_NAME = '$undefined$'

logger = logging.getLogger(__name__)


def get_single_tag_keys(parsed_label_config, control_type, object_type):
    """
    Gets parsed label config, and returns data keys related to the single control tag and the single object tag schema
    (e.g. one "Choices" with one "Text")
    :param parsed_label_config: parsed label config returned by "label_studio.misc.parse_config" function
    :param control_type: control tag str as it written in label config (e.g. 'Choices')
    :param object_type: object tag str as it written in label config (e.g. 'Text')
    :return: 3 string keys and 1 array of string labels: (from_name, to_name, value, labels)
    """
    assert len(parsed_label_config) == 1
    from_name, info = list(parsed_label_config.items())[0]
    assert info['type'] == control_type, 'Label config has control tag "<' + info['type'] + '>" but "<' + control_type + '>" is expected for this model.'  # noqa

    assert len(info['to_name']) == 1
    assert len(info['inputs']) == 1
    assert info['inputs'][0]['type'] == object_type
    to_name = info['to_name'][0]
    value = info['inputs'][0]['value']
    return from_name, to_name, value, info['labels']


def is_skipped(completion):
    if len(completion['annotations']) != 1:
        return False
    completion = completion['annotations'][0]
    return completion.get('skipped', False) or completion.get('was_cancelled', False)


def get_choice(completion):
    return completion['annotations'][0]['result'][0]['value']['choices'][0]


def get_image_local_path(url, image_cache_dir=None, project_dir=None, image_dir=None):
    return get_local_path(url, image_cache_dir, project_dir, get_env('HOSTNAME'), image_dir)


def get_image_size(filepath):
    return Image.open(filepath).size


def deploy_to_gcp_rest(args):
    # Setup env before hand: https://cloud.google.com/run/docs/setup
    # Prepare dirs with code and docker file
    #create_dir(args)
    # Set configuration params
    region = "us-central1"
    project_id = "i-portfolio-339416"
    service_name = args.project_name
    output_dir = os.path.join(args.root_dir, args.project_name)
    time_stamp = str(datetime.now().timestamp())
    # create tgz file to upload
    output_filename = os.path.join(output_dir, f"{time_stamp}.tgz")
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(output_dir, arcname=".")
    # get current credentials and project
    #credentials, project = google.auth.default()
    credentials, project = google.auth.load_credentials_from_file(r"C:\projects\Heartex\TestData\gcs\i-portfolio-339416-807c5a11ea6f.json")
    artifact_registry_name = 'cloud-run-source-deploy'
    #TO GCP
    # get registry
    url1 = f"https://artifactregistry.googleapis.com/v1beta2/projects/{project_id}/locations/{region}/repositories/{artifact_registry_name}?alt=json"
    registry_client = artifactregistry_v1beta2.ArtifactRegistryClient(credentials=credentials)
    try:
        repo_name = f"projects/{project_id}/locations/{region}/repositories/{artifact_registry_name}"
        repo = registry_client.get_repository(name=repo_name)
    except NotFound:
        if not repo:
            create_repository_request = CreateRepositoryRequest()
            #create_repository_request.repository_id = 'cloud-run-source-deploy'
            create_repository_request.repository = Repository()
            create_repository_request.repository.name = repo_name
            create_repository_request.repository.description = 'Cloud Run Source Deployments'
            create_repository_request.repository.format_ = Repository.Format.DOCKER
            repo = registry_client.create_repository(create_repository_request)
    except Exception as e:
        logger.error("Error while creating Artifact Repository.", exc_info=True)
        logger.error(e)

    # check if there are no such service
    url2 = f"https://{region}-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/{project_id}/services/{service_name}?alt=json"
    # Check permissions
    url3 = f"https://{region}-run.googleapis.com/v1/projects/{project_id}/locations/{region}/services/{service_name}:testIamPermissions?alt=json"

    storage_client = google_storage.Client(project=project_id, credentials=credentials)
    # Get storage link
    bucket_name = f"{project_id}_cloudbuild"
    bucket = storage_client.lookup_bucket(bucket_name)
    if not bucket:
        bucket = storage_client.create_bucket(bucket_name, project=project_id)
    url4 = f"https://storage.googleapis.com/storage/v1/b/{project_id}_cloudbuild?alt=json"
    url5 = f"https://storage.googleapis.com/storage/v1/b?alt=json&maxResults=1000&prefix={project_id}_cloudbuild&project={project_id}"

    # upload files POST
    with open(output_filename, mode='rb') as file:
        blob = bucket.blob(f"{time_stamp}.tgz")
        blob.upload_from_file(file)
    url6 = f"https://storage.googleapis.com/upload/storage/v1/b/i-portfolio-339416_cloudbuild/o?alt=json&name=source%2F1643289268.053218-f69504fdcb544157a1e69e10688f73de.tgz&uploadType=multipart"
    data_to_upload_gzip = ""
    # Post build

    build_client = cloudbuild_v1.CloudBuildClient(credentials=credentials)

    build = cloudbuild_v1.Build()
    build.images = [f"us-central1-docker.pkg.dev/i-portfolio-339416/{artifact_registry_name}/{service_name}"]
    build.source = Source()
    build.source.storage_source = StorageSource()
    build.source.storage_source.bucket = bucket_name
    build.source.storage_source.generation = blob.generation
    build.source.storage_source.object_ = f"{time_stamp}.tgz"
    build.steps = [{"args": ["build", "--network", "cloudbuild", "--no-cache", "-t",
                            f"us-central1-docker.pkg.dev/{project_id}/{artifact_registry_name}/{service_name}",
                            "."], "name": "gcr.io/cloud-builders/docker"}]

    build_operation = build_client.create_build(project_id=project_id, build=build)

    build_result = build_operation.result()

    artifact = build_result.artifacts.images[0]
    #url7 = f"https://cloudbuild.googleapis.com/v1/projects/i-portfolio-339416/locations/global/builds?alt=json"


    # Get build status (build id extracted from prev request
    build_id = "ZGI4ODI5OWUtMDM0OS00MzlkLTgwZDAtYWRlMjhkMzZhMzI1"
    url8 = f"https://cloudbuild.googleapis.com/v1/operations/build/i-portfolio-339416/ZGI4ODI5OWUtMDM0OS00MzlkLTgwZDAtYWRlMjhkMzZhMzI1?alt=json"
    # Wait for status "status": "SUCCESS"

    # POST services from project
    url9 = f"https://us-central1-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/i-portfolio-339416/services?alt=json"
    data_to_services = {"apiVersion": "serving.knative.dev/v1",
                        "kind": "Service",
                        "metadata": {"annotations": {
                            "client.knative.dev/user-image": "us-central1-docker.pkg.dev/i-portfolio-339416/cloud-run-source-deploy/simpletextclassifier",
                            "run.googleapis.com/client-name": "gcloud", "run.googleapis.com/client-version": "370.0.0"},
                            "labels": {},
                            "name": "simpletextclassifier",
                            "namespace": "i-portfolio-339416"},
                        "spec": {"template": {"metadata": {"annotations": {
                            "client.knative.dev/user-image": "us-central1-docker.pkg.dev/i-portfolio-339416/cloud-run-source-deploy/simpletextclassifier",
                            "run.googleapis.com/client-name": "gcloud", "run.googleapis.com/client-version": "370.0.0"},
                            "labels": {}, "name": "simpletextclassifier-00001-hut"},
                            "spec": {"containers": [{
                                "image": "us-central1-docker.pkg.dev/i-portfolio-339416/cloud-run-source-deploy/simpletextclassifier@sha256:259744734e1d4f0969bcbb83d95e485adf21439961ca5ed3452915fd7866907b"}]}}},
                        "status": {"address": {}}}

    # Get IAM policy key
    url10 = f"https://run.googleapis.com/v1/projects/i-portfolio-339416/locations/us-central1/services/simpletextclassifier:getIamPolicy?alt=json"
    etag = ""
    # Post IAM policy to service
    url11 = f"https://run.googleapis.com/v1/projects/i-portfolio-339416/locations/us-central1/services/simpletextclassifier:setIamPolicy?alt=json"
    data_iam_policy = {"policy": {"bindings": [{"members": ["allUsers"], "role": "roles/run.invoker"}], "etag": "BwXWfza0RE4="}}

    # Get revision
    url12 = f"https://us-central1-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/i-portfolio-339416/services/simpletextclassifier?alt=json"
    answer = {"traffic": [
      {
        "revisionName": "simpletextclassifier-00001-hut",
        "percent": 100,
        "latestRevision": True
      }
    ],
        "url": "https://simpletextclassifier-7zgkthkvcq-uc.a.run.app",
        "address": {
            "url": "https://simpletextclassifier-7zgkthkvcq-uc.a.run.app"
        }
    }
    # Routing traffic
    url13 = f"https://us-central1-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/i-portfolio-339416/services/simpletextclassifier?alt=json"
    url14 = f"https://us-central1-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/i-portfolio-339416/services/simpletextclassifier?alt=json"
    # PORT=9090 gcloud run deploy --source .
    service_url ="https://simpletextclassifier-7zgkthkvcq-uc.a.run.app"
