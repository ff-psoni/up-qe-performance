# Register `--env` Argument for Dynamic Host Selection
import json
from pathlib import Path

from locust import HttpUser, between, events


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--env", type=str, help="Environment (dev/stg/prod)", default="dev", required=True)
    parser.add_argument("--team", type=str, help="team name where config is stored", required=True) #capability


# Set `host` Before Locust Starts
@events.init.add_listener
def set_host(environment, **kwargs):
    """Set the host dynamically based on `--env`"""
    env = environment.parsed_options.env if hasattr(environment, "parsed_options") else "dev"
    team = environment.parsed_options.team if hasattr(environment, "parsed_options") else None

    config_path = Path(__file__).resolve().parent.parent / f"config/{team}/config.json"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    #read config.json
    with open(config_path, "r") as file:
        config = json.load(file)

    BaseTest.host = config[env]["baseUrl"] # Set the host
    print(f"🔹 Locust Host Set: {BaseTest.host}")


# Define BaseTest Class
class BaseTest(HttpUser):
    wait_time = between(1, 2)  # Simulate wait time between requests
    abstract = True  # marking it as abstract = True as we intend to subclass it

    def get_access_token(self):
        """To be implemented in service-specific classes."""
        raise NotImplementedError("Each service should define its own get_access_token.")

    def log_request_failure(self, endpoint, resp, logger):
        """
        Logs request failure details and reports it to Locust.

        :param endpoint: The API endpoint being tested.
        :param resp: The response object from the request.
        """
        error_message = (
            f"Request Failed | Endpoint: {endpoint} | "
            f"Status: {resp.status_code} | Reason: {resp.text} | "
            f"Response Time: {resp.elapsed.total_seconds()}s"
        )

        # Log the failure to Locust
        resp.failure(error_message)

        # Log in structured JSON format (useful for log aggregators)
        logger.error({
            "event": "request_failure",
            "endpoint": endpoint,
            "status_code": resp.status_code,
            "reason": resp.text,
            "response_time": resp.elapsed.total_seconds()
        })