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


def get_pdf_embed_key_for_current_stack() -> str:
    status = get_bluegreen_status_for_current_stack()
    config = pulumi.Config()
    key = config.require(f"{status}_pdf_embed_key")
    print(f"Pulumi is using PDF embed key for stack {pulumi.get_stack()}")
    return key


def get_self_registration_enabled_for_current_stack() -> str:
    status = get_bluegreen_status_for_current_stack()
    config = pulumi.Config()
    is_enabled = config.require(f"{status}_self_registration_enabled")
    print(
        f"Pulumi is setting self registration to {is_enabled} "
        f"for stack {pulumi.get_stack()}"
    )
    return is_enabled
