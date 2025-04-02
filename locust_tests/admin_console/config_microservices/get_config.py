import logging
from datetime import date
import random

from locust import task, between, TaskSet

from locust_tests.admin_console.ac_ms_base_http_user import ConfigMicroservicesBaseHTTPUser
from utils.logger import get_logger

logger = get_logger(__name__)

FEATURES = [
    "0da6131e-cfb2-4878-992f-123065813ee7/tenants/11111111-222a-3bbb-444c-d5e555555555",  #TENANT_CONFIGURATION
    "068f5559-a0ee-4021-8fd0-1640cb865117/tenants/11111111-222a-3bbb-444c-d5e555555555",  #GLOBAL_TENANT_CONFIGURATION
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


