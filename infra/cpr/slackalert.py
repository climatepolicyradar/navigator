import requests
import pulumi
import os


def _post_message(webhook_url: str, msg: str):
    # from https://docs.github.com/en/actions/learn-github-actions/environment-variables#default-environment-variables
    user = os.environ.get("GITHUB_ACTOR", os.environ.get("USER", "Anon"))
    is_ci = bool(os.environ.get("CI", False))

    is_ci_msg = "on CI" if is_ci else "outside of CI"
    stack = pulumi.get_stack()

    message = f"{stack} is being deployed by {user} {is_ci_msg}."

    if msg:
        message += f" {msg}"

    try:
        requests.post(webhook_url, json={"text": message})
    except Exception as e:
        print("Could not alert CPR about the current deployment. " + str(e))


def alert_slack(msg: str = ""):
    config = pulumi.Config()
    slack_webhook = config.require_secret("slack_webhook_url")
    slack_webhook.apply(lambda url: _post_message(url, msg))
