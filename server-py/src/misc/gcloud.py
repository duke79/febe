import os
import uuid
from contextlib import contextmanager

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from lib.py.core.paths import res_path
from lib.py.misc.secure import TemporarilyUnsecure

## Init fields
GOOGLE_ACCOUNT_NAME = "pulkitsingh01"
GCLOUD_PROJECT_NAME = "VilokanLabs"
GCLOUD_PROJECT_ID = "vilokanlabs-e8847"
GCLOUD_PROJECT_NUMBER = "422886694568"
GCLOUD_COMPUTE_ENGINE_UID = "105341384773385712840"
GCLOUD_COMPUTE_ENGINE_EMAIL = "422886694568-compute@developer.gserviceaccount.com"
GCLOUD_COMPUTE_INSTANCE = "instance-1"
GCLOUD_COMPUTE_ZONE = "us-east1-b"
GCLOUD_APP_ENGINE_UID = "114159396072215627810"
GCLOUD_APP_ENGINE_EMAIL = "vilokanlabs-e8847@appspot.gserviceaccount.com"


@contextmanager
def service_key():
    service_key = os.path.join(res_path, "vilokanlabs-e8847-7a01bd18328c.json")
    with TemporarilyUnsecure(service_key, keep=False) as service_key_unsecure:
        yield service_key_unsecure


def compute_engine():
    ## Decrypt GCLOUD Service key
    with service_key() as service_key_unsecure:
        try:
            ## GCLOUD API
            ComputeEngine = get_driver(Provider.GCE)
            # Note that the 'PEM file' argument can either be the JSON format or
            # the P12 format.
            driver = ComputeEngine(GCLOUD_COMPUTE_ENGINE_EMAIL, service_key_unsecure,
                                   project=GCLOUD_PROJECT_ID)
            proj = driver.ex_get_project()
            print(proj)
            for node in driver.list_nodes():
                print(node)
        except Exception as e:
            print(e)


def transfer_file(file_path):
    os.system("gcloud compute scp %s [INSTANCE_NAME]:~" % (file_path))


def transfer_dir(local_dir_path):
    os.system("gcloud compute scp --recurse [INSTANCE_NAME]:[REMOTE_DIR] %s " % local_dir_path)


def ssh_client():
    os.system("gcloud compute ssh %s  --zone %s" % (GCLOUD_COMPUTE_INSTANCE, GCLOUD_COMPUTE_ZONE))


def ssh_run(in_cmd="ls"):
    cmd = "gcloud compute ssh --zone {0} {1} --command \"{2}\"".format(GCLOUD_COMPUTE_ZONE, GCLOUD_COMPUTE_INSTANCE,
                                                                       in_cmd)
    os.system(cmd)


def git_configure():
    cmd1 = '''git config --global http.cookiefile "%USERPROFILE%\.gitcookies"'''
    cmd2 = '''powershell -noprofile -nologo -command Write-Output "source.developers.google.com`tFALSE`t/`tTRUE`t2147483647`to`tgit-PulkitSingh01.gmail.com=1/JGYdLiwAq1g8V0QT0aGTOnXfqXSBjkPjH6accEbnibnYVt142EiVmB9-DRHk68Lj" >>"%USERPROFILE%\.gitcookies"'''
    bash1 = '''
     eval 'set +o history' 2>/dev/null || setopt HIST_IGNORE_SPACE 2>/dev/null
     touch ~/.gitcookies
     chmod 0600 ~/.gitcookies
    
     git config --global http.cookiefile ~/.gitcookies
    
     tr , \\t <<\__END__ >>~/.gitcookies
    source.developers.google.com,FALSE,/,TRUE,2147483647,o,git-PulkitSingh01.gmail.com=1/JGYdLiwAq1g8V0QT0aGTOnXfqXSBjkPjH6accEbnibnYVt142EiVmB9-DRHk68Lj
    __END__
    eval 'set -o history' 2>/dev/null || unsetopt HIST_IGNORE_SPACE 2>/dev/null
    '''
    os.system(cmd1)
    os.system(cmd2)


def git_remote(repo="vilokanlabs"):
    """
    ref1: https://cloud.google.com/source-repositories/docs/pushing-code-from-a-repository
    ref2: https://source.cloud.google.com/repos
    :param repo:
    :return:
    """
    cmd = "git remote add google https://source.developers.google.com/p/%s/r/%s" % (
        GCLOUD_PROJECT_ID, repo
    )
    # os.system(cmd)
    cmd2 = "git remote add google ssh://pulkitsingh01@gmail.com@source.developers.google.com:2022/p/vilokanlabs-e8847/r/vilokanlabs"
    print(cmd2)
    # os.system(cmd2)


def spin_compute(name=uuid.uuid4()):
    """
    ref: https://codelabs.developers.google.com/codelabs/bake-and-deploy-pipeline/#1
    :return:
    """
    cmd = "gcloud compute instances create {instance_name} \
    --project {project_name} \
    --zone {zone} \
    --image spinnaker-codelab \
    --image-project marketplace-spinnaker-release \
    --machine-type {machine_type} \
    --scopes cloud-platform \
    --metadata startup-script=/var/spinnaker/startup/first_codelab_boot.sh,gce_account={google_account}".format_map(
        {
            "instance_name": name,
            "project_name": GCLOUD_PROJECT_ID,
            "zone": GCLOUD_COMPUTE_ZONE,
            "machine_type": "f1-micro",
            "google_account": GOOGLE_ACCOUNT_NAME
        }
    )
    os.system(cmd)


def spin_ssh(name="a4254d00-39fa-4ccd-998a-f021c1b95a35"):
    cmd = 'gcloud compute ssh {instance_name} \
    --project {project_name} \
    --zone {zone} \
    --ssh-flag="-L 8084:localhost:8084" \
    --ssh-flag="-L 9000:localhost:9000" \
    --ssh-flag="-L 5656:localhost:5656"'.format_map(
        {
            "instance_name": name,
            "project_name": GCLOUD_PROJECT_ID,
            "zone": GCLOUD_COMPUTE_ZONE
        }
    )
    print(cmd)


def git_push():
    os.system("git push google master:master")


def deploy(repo="vilokanlabs"):
    """
    ref: https://cloud.google.com/sdk/gcloud/reference/source/repos/clone
    :param repo:
    :return:
    """
    cmd = '''gcloud source repos clone {0}
             cd {0}
             gcloud app deploy app.yaml'''.format(repo)
    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    compute_engine()


def app_engine_deploy():
    cmd_create_repo = "gcloud source repos create hello-world"
    cmd_clone_repo = "gcloud source repos clone hello-world"
    cmd_deploy = "gcloud app deploy app.yaml"


def compute_engine_prepare():
    """
    ref1: https://codelabs.developers.google.com/codelabs/cp100-compute-engine/#3
    ref2: https://cloud.google.com/python/tutorials/bookshelf-on-compute-engine
    :return:
    """
    cmd1 = 'gcloud compute firewall-rules create default-allow-http-8080 \
  --allow tcp:8080 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server \
  --description "Allow port 8080 access to http-server"'
