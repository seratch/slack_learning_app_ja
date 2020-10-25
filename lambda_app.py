import logging
import os
from logging import Logger
from typing import Optional, Dict

from slack_bolt import BoltContext, App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow import LambdaS3OAuthFlow
from slack_bolt.authorization import AuthorizeResult
from slack_bolt.authorization.authorize import Authorize
from slack_bolt.oauth.callback_options import CallbackOptions
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.errors import SlackApiError
from slack_sdk.oauth import InstallationStore
from slack_sdk.oauth.installation_store import Bot, Installation

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

# https://github.com/slackapi/python-slackclient/pull/860
class CacheableInstallationStore(InstallationStore):
    cached_bots: Dict[str, Bot] = {}

    def __init__(self, installation_store: InstallationStore):
        self.underlying = installation_store

    @property
    def logger(self) -> Logger:
        return self.underlying.logger

    def save(self, installation: Installation):
        self.underlying.save(installation)

    def find_bot(
        self, *, enterprise_id: Optional[str], team_id: Optional[str]
    ) -> Optional[Bot]:
        key = f"{enterprise_id}-{team_id}"
        if key in self.cached_bots:
            return self.cached_bots[key]
        bot = self.underlying.find_bot(enterprise_id=enterprise_id, team_id=team_id)
        if bot:
            self.cached_bots[key] = bot
        return bot

# https://github.com/slackapi/bolt-python/pull/122
class InstallationStoreAuthorize(Authorize):
    authorize_result_cache: Dict[str, AuthorizeResult] = {}

    def __init__(
        self,
        *,
        logger: Logger,
        installation_store: InstallationStore,
        cache_enabled: bool = False,
    ):
        self.logger = logger
        self.installation_store = installation_store
        self.cache_enabled = cache_enabled

    def __call__(
        self,
        *,
        context: BoltContext,
        enterprise_id: Optional[str],
        team_id: str,
        user_id: Optional[str],
    ) -> Optional[AuthorizeResult]:
        bot: Optional[Bot] = self.installation_store.find_bot(
            enterprise_id=enterprise_id,
            team_id=team_id,
        )
        if bot is None:
            self.logger.debug(
                f"No installation data found "
                f"for enterprise_id: {enterprise_id} team_id: {team_id}"
            )
            return None

        if self.cache_enabled and bot.bot_token in self.authorize_result_cache:
            return self.authorize_result_cache[bot.bot_token]
        try:
            auth_result = context.client.auth_test(token=bot.bot_token)
            authorize_result = AuthorizeResult.from_auth_test_response(
                auth_test_response=auth_result,
                bot_token=bot.bot_token,
                user_token=None,  # Not yet supported
            )
            if self.cache_enabled:
                self.authorize_result_cache[bot.bot_token] = authorize_result
            return authorize_result
        except SlackApiError as err:
            self.logger.debug(
                f"The stored bot token for enterprise_id: {enterprise_id} team_id: {team_id} "
                f"is no longer valid. (response: {err.response})"
            )
            return None


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
