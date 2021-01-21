import logging
logging.basicConfig(level=logging.DEBUG)

import os

from slack_bolt import App
from slack_bolt.oauth.callback_options import CallbackOptions
from slack_bolt.oauth.oauth_settings import OAuthSettings

from app.listeners import register_listeners

# デフォルトではローカルファイルに state の情報やインストール情報を書きます
# 必要に応じて別の実装に差し替えてください（Amazon S3, RDB に対応しています）
from app.onboarding import install_completion, install_failure

app = App(
    oauth_settings=OAuthSettings(
        callback_options=CallbackOptions(
            success=install_completion, failure=install_failure
        ),
        # Simpler & v1.0.x compatible mode
        installation_store_bot_only=True
    )
)
register_listeners(app)

from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/slack/install", methods=["GET"])
def install():
    return handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return handler.handle(request)


# Only for local debug
if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    flask_app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
