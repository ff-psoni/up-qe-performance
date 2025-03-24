from locust import task, TaskSet, constant_pacing

from base.base_user import BaseTest
from utils.logger import logger


class Service_Task(TaskSet):

    @task
    def get_users(self):
        logger.info("Started API : /api121/users")
        endpoint = "/api/users"
        with self.client.get(endpoint, name="Get Users", catch_response=True) as response:
            print(f"Response is :  {response.request.url} and status code {response.status_code}" )
            if response.status_code != 200:
                self.user.log_request_failure(endpoint, response, logger)

class MyUser(BaseTest):


    print("Inside MyUser")

    wait_time = constant_pacing(2)
    tasks = [Service_Task]

