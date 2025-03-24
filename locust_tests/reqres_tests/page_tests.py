from locust import task, TaskSet, constant_pacing

from base.base_task import BaseTest
from utils.logger import logger


class Service_Task(TaskSet):

    @task
    def get_users(self):
        logger.info("Started API : /api121/users")
        with self.client.get("/api/users", name="/api/users", catch_response=True) as response:
            print(f"Response is :  {response.request.url} and status code {response.status_code}" )

            if response.status_code != 200:
                response.failure(f"Failed to get users using endpoint {response.request.url} : response code : {response.status_code} and reason : {response.text}" )
                logger.error(f"Failed to get users: {response.request.url}")

class MyUser(BaseTest):


    print("Inside MyUser")

    wait_time = constant_pacing(2)
    tasks = [Service_Task]

