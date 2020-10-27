import logging
import os

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow import LambdaS3OAuthFlow
from slack_bolt.authorization.authorize import InstallationStoreAuthorize
from slack_bolt.oauth.callback_options import CallbackOptions
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store.cacheable_installation_store import CacheableInstallationStore

from app.listeners import register_listeners
from app.onboarding import install_failure, install_completion

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

oauth_flow = LambdaS3OAuthFlow(
    settings=OAuthSettings(
        install_path=os.environ["SLACK_LAMBDA_PATH"],
        redirect_uri_path=os.environ["SLACK_LAMBDA_PATH"],
        callback_options=CallbackOptions(
            success=install_completion, failure=install_failure
        ),
    )
)

oauth_flow.settings.installation_store = CacheableInstallationStore(
    oauth_flow.settings.installation_store
)
oauth_flow.settings.authorize = InstallationStoreAuthorize(
    logger=oauth_flow.logger,
    installation_store=oauth_flow.settings.installation_store,
    cache_enabled=True,
)

app = App(
    process_before_response=True,  # This is required when you can Bolt apps on FaaS
    oauth_flow=oauth_flow,
)
register_listeners(app)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


if __name__ == "__main__":
    import lambda_local_dev

    lambda_local_dev.run(app)
