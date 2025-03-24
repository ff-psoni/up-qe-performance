# Register `--env` Argument for Dynamic Host Selection
import json
from pathlib import Path

from locust import HttpUser, between, events


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--env", type=str, help="Environment (dev/staging/prod)", default="dev", required=True)
    parser.add_argument("--team", type=str, help="team name where config is stored", required=True)


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
