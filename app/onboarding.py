import os
from typing import List, Optional

from slack_bolt import BoltResponse, Respond, Ack
from slack_bolt.oauth.callback_options import SuccessArgs, FailureArgs
from slack_sdk.errors import SlackApiError

install_path = os.environ["SLACK_LAMBDA_PATH"]
installation_message_text = (
    ":wave: インストールありがとうございます！このアプリを使って Slack プラットフォームの機能を一緒に学んでいきましょう！"
)


def build_installation_message_blocks(app_id: str, user_id: str) -> List[dict]:
    return [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "Slack アプリ開発へようこそ！"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":wave: インストールありがとうございます！\nこのアプリを使って Slack プラットフォームの機能を一緒に学んでいきましょう！",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"""
このアプリはこのワークスペースで有効化されました。

これは Slack の <https://api.slack.com/authentication/oauth-v2|OAuth フロー>を経て、このアプリにアクセストークンが付与され、ボットユーザーやこのアプリが提供する機能（ショートカットなど）がワークスペース内に追加されたことを意味します。

Slack アプリはこのワークスペースから付与されたアクセストークンを使ってチャンネルにメッセージを投稿したり、モーダルを開いたりします。

このアプリを削除するなどの管理操作は、いつでも<https://my.slack.com/apps/{app_id}|この URL> で行うことができます。
"""},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "メッセージの投稿は基本的な機能です。まずはじめに、このメッセージがどのように投稿されたかを簡単に説明します。"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "1. チャンネルや DM にメッセージを投稿するには <https://api.slack.com/methods/chat.postMessage|*chat.postMessage*> という API を使います。<https://api.slack.com/methods/chat.postMessage/test|*Tester タブ*>を使うと、API をブラウザから試すこともできます。",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "API ドキュメント"},
                "value": "chat.postMessage",
                "url": "https://api.slack.com/methods/chat.postMessage",
                "action_id": "link_button",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": """2. 内容は <https://api.slack.com/block-kit|*Block Kit*> という UI フレームワークで構成しています。右にあるのは標準コンポーネントの一例です。
""",
            },
            "accessory": {
                "type": "multi_users_select",
                "placeholder": {"type": "plain_text", "text": "ユーザーを選択"},
                "action_id": "message_multi_users_select",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"3. API で投稿するメッセージに<https://api.slack.com/apps|リンク>を埋め込んだり、こんな感じで <@{user_id}> 誰かをメンションするには、<https://api.slack.com/reference/surfaces/formatting|記法のドキュメント>を参照してください。テキストでの投稿でも Block Kit 内への埋め込みでも利用できます。",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "記法のドキュメント"},
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
                "text": """
Web API を使ってメッセージを投稿する、ファイルをアップロードする、などの操作はシンプルです。利用可能な API は https://api.slack.com/methods で確認することができます。

このアプリでは、それだけに留まらず、よりインタラクティブな Slack 連携アプリをつくるための方法を紹介しています。実際の機能が動作している様子を見ながら、楽しく体験しながら学んでいってください。

そして、このアプリのコードは公開されていますので、どのように実現されているかはソースコードを見比べながら確認することができます。

https://github.com/seratch/slack_learning_app_ja
""",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "次は *ホームタブ* にアクセスしてみましょう。この画面の上の方をみると「ホーム」というタブがあるので、クリックしてみてください。",
            },
        },
        {
            "type": "image",
            "title": {"type": "plain_text", "text": "タブ"},
            "image_url": "https://user-images.githubusercontent.com/19658/96687397-c717c280-13ba-11eb-8f24-f306d4ffa588.png",
            "alt_text": "タブ",
        },
    ]


def render_success_page(app_id: str, team_id: Optional[str]) -> str:
    url = (
        "slack://open" if team_id is None else f"slack://app?team={team_id}&id={app_id}"
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
<h2>インストールありがとうございます！</h2>
<p>Slack クライアントアプリに移動します... 遷移しない場合は<a href="{url}">こちら</a>をクリックしてください。</p>
</body>
</html>
"""


def render_failure_page(install_path: str, reason: str) -> str:
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
<h2>エラーが発生しました</h2>
<p><a href="{install_path}">こちら</a>からやり直すか、このアプリの管理者にお問い合わせください。 (エラー: {reason})</p>
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
                installation.app_id,
                installation.user_id
            ),
        )
        html = render_success_page(
            app_id=installation.app_id, team_id=installation.team_id
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
    respond(text=f"あなたは {users} を選択しました！", replace_original=False)
