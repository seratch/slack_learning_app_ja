import os
from typing import List, Optional

from slack_bolt import BoltResponse, Respond, Ack
from slack_bolt.oauth.callback_options import SuccessArgs, FailureArgs
from slack_sdk.errors import SlackApiError

lang = os.environ.get("SLACK_LANGUAGE")


def i18n(default: str, ja: str):
    if lang == "ja":
        return ja
    return default


install_path = os.environ["SLACK_LAMBDA_PATH"]
installation_message_text = i18n(
    ":wave: Thank you for installing this app! Let's learn the Slack Platform features step by step.",
    ":wave: インストールありがとうございます！このアプリを使って Slack プラットフォームの機能を一緒に学んでいきましょう！",
)


def build_installation_message_blocks(app_id: str, user_id: str) -> List[dict]:
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": i18n("Welcome to Slack App development!", "Slack アプリ開発へようこそ！"),
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    ":wave: Thank you for installing this app! Let's learn the Slack Platform features step by step.",
                    ":wave: インストールありがとうございます！\nこのアプリを使って Slack プラットフォームの機能を一緒に学んでいきましょう！",
                ),
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    f"""
This learning app has been enabled for this workspace for you. This app completed Slack's <https://api.slack.com/authentication/oauth-v2|OAuth flow> and acquired an access token for this workspace, and the apps' bot user and features are enabled in this workspace. Slack apps can post a message, open a modal with an access token.

You can delete this app at <https://my.slack.com/apps/{app_id}|this URL> at any time.
""",
                    f"""
このアプリはこのワークスペースで有効化されました。

これは Slack の <https://api.slack.com/authentication/oauth-v2|OAuth フロー>を経て、このアプリにアクセストークンが付与され、ボットユーザーやこのアプリが提供する機能（ショートカットなど）がワークスペース内に追加されたことを意味します。

Slack アプリはこのワークスペースから付与されたアクセストークンを使ってチャンネルにメッセージを投稿したり、モーダルを開いたりします。

このアプリを削除するなどの管理操作は、いつでも<https://my.slack.com/apps/{app_id}|この URL> で行うことができます。
""",
                ),
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    "Posting a message is a very basic feature. First off, let me explain how this message was posted in this direct message.",
                    "メッセージの投稿は基本的な機能です。まずはじめに、このメッセージがどのように投稿されたかを簡単に説明します。",
                ),
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    "1. To post a message in channel/DMs, Slack apps can use <https://api.slack.com/methods/chat.postMessage|*chat.postMessage*> API method. <https://api.slack.com/methods/chat.postMessage/test|*Tester tab*> is a useful tool to check how the API works in a web browser.",
                    "1. チャンネルや DM にメッセージを投稿するには <https://api.slack.com/methods/chat.postMessage|*chat.postMessage*> という API を使います。<https://api.slack.com/methods/chat.postMessage/test|*Tester タブ*>を使うと、API をブラウザから試すこともできます。",
                ),
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": i18n("API Document", "API ドキュメント"),
                },
                "value": "chat.postMessage",
                "url": "https://api.slack.com/methods/chat.postMessage",
                "action_id": "link_button",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """2. The message is composed using <https://api.slack.com/block-kit|*Block Kit*>, Slack's UI framework. Here is one built-in compoent.
""",
                    """2. 内容は <https://api.slack.com/block-kit|*Block Kit*> という UI フレームワークで構成しています。右にあるのは標準コンポーネントの一例です。
                             """,
                ),
            },
            "accessory": {
                "type": "multi_users_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": i18n("Select users", "ユーザーを選択"),
                },
                "action_id": "message_multi_users_select",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    f"3. To learn how to embed <https://api.slack.com/apps|links>, mention someone like this <@{user_id}> in API payloads, see <https://api.slack.com/reference/surfaces/formatting|this document>. You can use the same syntax in both `text` and `blocks`.",
                    f"3. API で投稿するメッセージに<https://api.slack.com/apps|リンク>を埋め込んだり、こんな感じで <@{user_id}> 誰かをメンションするには、<https://api.slack.com/reference/surfaces/formatting|記法のドキュメント>を参照してください。テキストでの投稿でも Block Kit 内への埋め込みでも利用できます。",
                ),
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": i18n("Formatting text", "記法のドキュメント"),
                },
                "value": "chat.postMessage",
                "url": "https://api.slack.com/reference/surfaces/formatting",
                "action_id": "link_button",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
It's quite simple and easy to post messages, upload files via Web APIs. You can find the list of available APIs at <https://api.slack.com/methods|api.slack.com/methods>.

This app helps you learn Slack's interactive features, beyond just sending API requests to Slack. With this app, you will learn by trying the interactive features in a fun way.

This app's source code is publicly available. You can check how the details are implemented by checking the code.

https://github.com/seratch/slack_learning_app_ja
                    """,
                    """
Web API を使ってメッセージを投稿する、ファイルをアップロードする、などの操作はシンプルです。利用可能な API は https://api.slack.com/methods で確認することができます。

このアプリでは、それだけに留まらず、よりインタラクティブな Slack 連携アプリをつくるための方法を紹介しています。実際の機能が動作している様子を見ながら、楽しく体験しながら学んでいってください。

そして、このアプリのコードは公開されていますので、どのように実現されているかはソースコードを見比べながら確認することができます。

https://github.com/seratch/slack_learning_app_ja
                    """,
                ),
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    "Next, try the *Home Tab*! There should be a tab named 'Home' at the top of this screen. Click the Home tab now",
                    "次は *ホームタブ* にアクセスしてみましょう。この画面の上の方をみると「ホーム」というタブがあるので、クリックしてみてください。",
                ),
            },
        },
        {
            "type": "image",
            "title": {"type": "plain_text", "text": i18n("Tab", "タブ")},
            "image_url": i18n(
                "https://user-images.githubusercontent.com/19658/97379935-57995a00-1909-11eb-9732-a93e65967ec8.png",
                "https://user-images.githubusercontent.com/19658/96687397-c717c280-13ba-11eb-8f24-f306d4ffa588.png",
            ),
            "alt_text": i18n("Tab", "タブ"),
        },
    ]


def render_success_page(
    app_id: str,
    team_id: Optional[str],
    is_enterprise_install: Optional[bool] = None,
    enterprise_url: Optional[str] = None,
) -> str:
    if (
        is_enterprise_install is True
        and enterprise_url is not None
        and app_id is not None
    ):
        url = f"{enterprise_url}manage/organization/apps/profile/{app_id}/workspaces/add"
    elif team_id is None or app_id is None:
        url = "slack://open"
    else:
        url = f"slack://app?team={team_id}&id={app_id}"
    main = i18n(
        f"""
<h2>Thank you!</h2>
<p>Redirecting to the Slack App... click <a href="{url}">here</a></p>
""",
        f"""
<h2>インストールありがとうございます！</h2>
<p>Slack クライアントアプリに移動します... 遷移しない場合は<a href="{url}">こちら</a>をクリックしてください。</p>
""",
    )
    return f"""
<html>
<head>
<meta http-equiv="refresh" content="0; URL={url}">
<style>
body {{
  padding: 10px 15px;
  font-family: verdana;
  text-align: center;
}}
</style>
</head>
<body>
{main}
</body>
</html>
"""


def render_failure_page(install_path: str, reason: str) -> str:
    main = i18n(
        f"""
<h2>Oops, Something Went Wrong!</h2>
<p>Please try again from <a href="{install_path}">here</a> or contact the app owner (reason: {reason})</p>
""",
        f"""
<h2>エラーが発生しました</h2>
<p><a href="{install_path}">こちら</a>からやり直すか、このアプリの管理者にお問い合わせください。 (エラー: {reason})</p>
""",
    )
    return f"""
<html>
<head>
<style>
body {{
  padding: 10px 15px;
  font-family: verdana;
  text-align: center;
}}
</style>
</head>
<body>
{main}
</body>
</html>
"""


def install_completion(args: SuccessArgs):
    installation = args.installation
    client = args.request.context.client
    try:
        client.chat_postMessage(
            token=installation.bot_token,
            channel=installation.user_id,
            text=installation_message_text,
            blocks=build_installation_message_blocks(
                installation.app_id, installation.user_id
            ),
        )
        html = render_success_page(
            app_id=installation.app_id,
            team_id=installation.team_id,
            is_enterprise_install=installation.is_enterprise_install,
            enterprise_url=installation.enterprise_url,
        )
        return BoltResponse(
            status=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": len(bytes(html, "utf-8")),
            },
            body=html,
        )
    except SlackApiError as e:
        html = render_failure_page(install_path, e.response["error"])
        return BoltResponse(
            status=500,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Content-Length": len(bytes(html, "utf-8")),
            },
            body=html,
        )


def install_failure(args: FailureArgs):
    html = render_failure_page(install_path, args.reason)
    return BoltResponse(
        status=args.suggested_status_code,
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": len(bytes(html, "utf-8")),
        },
        body=html,
    )


def message_multi_users_select(ack: Ack):
    ack()


def message_multi_users_select_lazy(action: dict, respond: Respond):
    users = ", ".join([f"<@{u}>" for u in action["selected_users"]])
    respond(
        text=i18n(f"You selected {users}!", f"あなたは {users} を選択しました！"),
        replace_original=False,
    )
