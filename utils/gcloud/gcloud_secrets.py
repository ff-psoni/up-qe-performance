import json

from google.cloud import secretmanager_v1


def access_latest_secret_version(project_id, secret_id):
    """
    Accesses GCP Secrets Manager for the project and gets the latest secret from the container. Per uRFC 70 secret
        access should always point to the latest version.
    Returns:
        secret (dict): This is the secret from GCP, it is stored as a JSON, which will be converted into a python
            dictionary.
    """
    client = secretmanager_v1.SecretManagerServiceClient()
    accessed_secret_version_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    request = {
        "name": accessed_secret_version_name
    }
    accessed_secret_version = client.access_secret_version(request=request)
    secret = accessed_secret_version.payload.data.decode('UTF-8')
    return json.loads(secret)
