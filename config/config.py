import json

from types import SimpleNamespace
from utils.gcloud.gcloud_secrets import access_latest_secret_version

DEV_PROJECT_ID = "up-qe-api-plus-dev-rotw-e7e3"
STG_PROJECT_ID = "up-qe-api-plus-stg-rotw-6ffe"
UAT_PROJECT_ID = "up-qe-api-plus-uat-rotw-3e25"
PRD_PROJECT_ID = "up-qe-api-plus-prd-rotw-8e5d"
SECRET_ID = "qe-api-plus-secret-container"

def config(env="STG", local=False):
    if env == "DEV":
        PROJECT_ID = DEV_PROJECT_ID
    elif env == "STG":
        PROJECT_ID = STG_PROJECT_ID
    elif env == "UAT":
        PROJECT_ID = UAT_PROJECT_ID
    elif env == "PRD":
        PROJECT_ID = PRD_PROJECT_ID
    else:
        raise ValueError(f"Invalid environment: {env}")
    if local is True:
        with open("config.json") as f:
            secrets = json.loads(f.read())
            processed_secrets = SimpleNamespace(**secrets)
        return processed_secrets
    else:
        secrets = access_latest_secret_version(PROJECT_ID, SECRET_ID)
        processed_secrets = SimpleNamespace(**secrets)
        return processed_secrets