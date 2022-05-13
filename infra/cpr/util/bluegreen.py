import json
import pulumi


def get_bluegreen_config() -> dict:
    with open("blue-green-status.json", "r") as bluegreen_file:
        data = json.load(bluegreen_file)
        print(f"Pulumi is using blue-green config: {data}")
        return data


def get_bluegreen_status_for_current_stack() -> str:
    bluegreen_config = get_bluegreen_config()
    bluegreen_status_for_current_stack = bluegreen_config[pulumi.get_stack()]
    return bluegreen_status_for_current_stack


def get_app_domain_for_current_stack() -> str:
    status = get_bluegreen_status_for_current_stack()
    config = pulumi.Config()
    domain = config.require(f"{status}_domain")
    print(f"Pulumi is using domain {domain} for stack {pulumi.get_stack()}")
    return domain
