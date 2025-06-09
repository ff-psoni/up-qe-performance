from datetime import date
import random

from locust import task, between

from base.ac_ms_base_http_user import ConfigMicroservicesBaseHTTPUser
from utils.logger import get_logger

logger = get_logger(__name__)

FEATURES = [
    "ee17b472-dd90-4fb3-8128-444c4e7bf6b9/tenants/8c1d676b-f167-520f-a82b-eb0224b0163d" #EMERSON_API_CREDENTIALS
    ]


class ReadConfig(ConfigMicroservicesBaseHTTPUser):

    wait_time = between(2, 3)
    weight = 1

    @task
    def get_config(self):
        feature = random.choice(FEATURES)
        endpoint = "/configs/features/" + feature
        headers = self._get_headers()
        with self.client.get(endpoint, headers=headers, name="/config", catch_response=True) as resp:
            print("Endpoint is : ", endpoint)
            print(f"/config:{resp.status_code}, {date.today()}")
            if resp.status_code != 200:
                self.log_request_failure(endpoint, resp, logger)


