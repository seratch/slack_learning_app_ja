import datetime
import json
import os
from logging import Logger

from slack_bolt import BoltContext, Ack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

lang = os.environ.get("SLACK_LANGUAGE")


def i18n(default: str, ja: str):
    if lang == "ja":
        return ja
    return default


pages = [
    # --------------------------------------------
    # page 1
    # --------------------------------------------
    [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": i18n("1. Home Tab", "1. ホームタブ")},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
This page is the Home Tab. In this first tutorial page, you will learn how the home tab is built. Although we use Home tab for displaying tutorial content here, you can use it for showing a list of pending approval requests or building a data dashboard. The <https://my.slack.com/apps/ADZ494LHY|Google Calendar App>'s Home tab is a great example.

The Home Tab is not enabled by default. Go to the Slack App Configuration page, and turn *Features* > *App Home* on.

You can use <http://api.slack.com/methods/views.publish|*views.publish*> API method for refreshing Home tabs. The API, which requires `user_id` and `view`, updates the whole tab view for each user.
```
{
	"type": "home",
	"blocks": [
		{"type": "section", "text": {"type": "mrkdwn", "text": "This page is the Home Tab."}},
		{"type": "divider"}
	]
}
```
                """,
                    """
このページは「ホームタブ」と呼ばれるものです。最初のチュートリアルでは、このホームタブがどのように作られているかを説明します。ここではチュートリアルの表示に利用していますが、未対応の承認依頼一覧を表示したり、ダッシュボードを構成すると便利です。<https://my.slack.com/apps/ADZ494LHY|Google カレンダーアプリ>のホームタブはとてもよくできていますので、参考にしてみてください。

ホームタブはデフォルトでは有効になっていない機能です。Slack アプリの管理画面の *Features* > *App Home* で有効にしておいてください。

タブの設定・更新には <http://api.slack.com/methods/views.publish|*views.publish*> という API を使います。更新するときは、最新の状態の見た目を構築して、全体をまるっと上書きする形になります。この API には `user_id` と `view` を渡して、ユーザーごとに設定してます。
```
{
	"type": "home",
	"blocks": [
		{"type": "section", "text": {"type": "mrkdwn", "text": "このページは「ホームタブ」と呼ばれるものです。"}},
		{"type": "divider"}
	]
}
```
                """,
                ),
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
As with the welcome message, you can place <https://api.slack.com/block-kit|*Block Kit*> components in Home tabs.
        """,
                    """
先ほどのメッセージと同様、ホームタブの中に <https://api.slack.com/block-kit|*Block Kit*> によるボタンやプルダウンを配置することができます。
        """,
                ),
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":star::star::star:"},
                    "value": "3",
                    "action_id": "page1_home_tab_button_3",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":star::star:"},
                    "value": "2",
                    "action_id": "page1_home_tab_button_2",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":star:"},
                    "value": "1",
                    "action_id": "page1_home_tab_button_1",
                },
                {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n("Select a user", "ユーザーを選択"),
                    },
                    "action_id": "page1_home_tab_users_select",
                },
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
Using <https://api.slack.com/events-api|*Events API*> is the common way to set up and maintain Home tab content. The <https://api.slack.com/events/app_home_opened|*app_home_opened*> event triggers when an end user access Home Tab. Your app can subscribe the event and update the tab for the user. Actually, the event triggered when you accessed this tab for the first time and this app updated the tab quickly.

It's also possible to update Home tabs at any time regardless of the end users' access. For instance, your app can update tabs as part of midnight batch processes and/or asking end users to manually click buttons to refresh the contents. In this tutorial app, this app never updates unless you click *Previous* or *Next* after the initial loading.

That's all about Home tabs here. Let's go to the next page by clicking the *Next* button.
""",
                    """
ホームタブの設定・更新タイミングは <https://api.slack.com/events-api|*Events API*> を使うのが一般的です。ユーザーがアクセスしたときに発生する <https://api.slack.com/events/app_home_opened|*app_home_opened*> というイベントを受け取るように Slack アプリを設定しておき、そのイベントが発生したら、対象ユーザー用のタブを更新します。あなたが先ほどこのタブを開いたとき、実はそのような処理が実行されていたのです。

ユーザーアクセス以外のタイミング以外で更新することもできます。バッチ処理で事前更新しておいたり、手動更新用のボタンを置いたりもできます。このチュートリアルは初回表示以外では *「前へ」* *「次へ」* などのボタンを押したときだけ更新されます。

ホームタブの説明は以上です。下にある *「次へ」* ボタンを押して次のページへ進みましょう。
""",
                ),
            },
        },
    ],
    # --------------------------------------------
    # page 2
    # --------------------------------------------
    [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": i18n("2. Modals", "2. モーダル")},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
Great! The Home tab has been successfully updated. The feature we learn here is Modals, which was already used a lot in the previous page. To enable this feature, go to the Slack App configuration page and turn *Features* > *Interactivity & Shortcuts* > *Interactivity* on and set a valid URL for *Request URL*.

You can open a new modal by clicking the following button. The modal has a few custom validation logics. Try the submission and see how the validations work.
""",
                    """
無事、ホームタブが更新されていますね。次に紹介する機能は、前のページで既に使われていた「モーダル」です。モーダルは、アプリ管理画面で *Features* > *Interactivity & Shortcuts* > *Interactivity* を有効にして Request URL を正しく設定するだけで利用することができます。

以下のボタンをクリックするとモーダルが起動します。入力チェックが実装されていますので、送信まで実行してみてください。
""",
                ),
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": i18n("Open a modal", "モーダルを起動する"),
                    },
                    "value": "3",
                    "style": "primary",
                    "action_id": "page2_modal",
                },
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
You can freely implement custom validation rules this way. Check this app's code for further details.

```
@app.view(callback_id)
def handle_modals(ack, view):
    values = view["state"]["values"]
    title = values["block_id"]["action_id"]["value"]
    errors = {}
    if len(title) < 8:
        errors["title"] = "Title must contain at least 8 characters"
    if len(errors) > 0:
        return ack(response_action="errors", errors=errors)  # Show errors on the modal
    # It's all set. You can store the data.
    ack()  # Closing the modal
```

You can use *Block Kit Builder* for learning modals without building actual Slack apps. Open <https://app.slack.com/block-kit-builder#%7B%22type%22:%22modal%22,%22title%22:%7B%22type%22:%22plain_text%22,%22text%22:%22My%20App%22,%22emoji%22:true%7D,%22blocks%22:%5B%5D%7D|this URL> in browser. You will see a blank preview. Cut and past the following JSON data in the right pane.

```
{"type": "modal", "callback_id": "page2_modal_submission", "title": {"type": "plain_text", "text": "New Task :pencil:"}, "submit": {"type": "plain_text", "text": "Submit"}, "close": {"type": "plain_text", "text": "Cancel"}, "blocks": [{"type": "input", "block_id": "title", "element": {"type": "plain_text_input", "action_id": "input", "initial_value": "Help!", "placeholder": {"type": "plain_text", "text": "Write the title"}}, "label": {"type": "plain_text", "text": "Title"}, "optional": false}, {"type": "input", "block_id": "assignee", "element": {"type": "users_select", "action_id": "input", "placeholder": {"type": "plain_text", "text": "Select an assignee"}}, "label": {"type": "plain_text", "text": "Assignee"}, "optional": true}, {"type": "input", "block_id": "priority", "element": {"type": "radio_buttons", "action_id": "input", "initial_option": {"text": {"type": "plain_text", "text": "Medium"}, "value": "m"}, "options": [{"text": {"type": "plain_text", "text": "High"}, "value": "h"}, {"text": {"type": "plain_text", "text": "Medium"}, "value": "m"}, {"text": {"type": "plain_text", "text": "Low"}, "value": "l"}]}, "label": {"type": "plain_text", "text": "Priority"}, "optional": false}, {"type": "input", "block_id": "deadline", "element": {"type": "datepicker", "action_id": "input", "initial_date": "2020-10-28", "placeholder": {"type": "plain_text", "text": "Select the due date"}}, "label": {"type": "plain_text", "text": "Due Date"}, "optional": true}, {"type": "input", "block_id": "description", "element": {"type": "plain_text_input", "action_id": "input", "initial_value": "ASAP!", "multiline": true, "placeholder": {"type": "plain_text", "text": "Write details as much as possible"}}, "label": {"type": "plain_text", "text": "Description"}, "optional": true}]}
```

You should see the exactly same modal there!

Check the <https://api.slack.com/surfaces/modals/using|API document> and <https://api.slack.com/tools/bolt|Bolt document> for furhther information.
""",
                    """
入力項目のバリデーションは以下のような形で自由に実装することができます。詳細はこのアプリのソースコードを見てみてください。

```
@app.view(callback_id)
def handle_modals(ack, view):
    values = view["state"]["values"]
    title = values["block_id"]["action_id"]["value"]
    errors = {}
    if len(title) < 8:
        errors["title"] = "件名は 8 文字以上で入力してください"
    if len(errors) > 0:
        return ack(response_action="errors", errors=errors)  # エラー表示を返す
    # 入力チェック OK なので、ここでデータを保存したりする
    ack()  # モーダルを閉じる
```

また、アプリを構築せずとも、このモーダルの見た目を *Block Kit Builder* で触ってみることができます。<https://app.slack.com/block-kit-builder#%7B%22type%22:%22modal%22,%22title%22:%7B%22type%22:%22plain_text%22,%22text%22:%22My%20App%22,%22emoji%22:true%7D,%22blocks%22:%5B%5D%7D|こちらの URL> にアクセスしてみてください。ブラウザで Slack ワークスペースにログインしていれば、すぐにプレビューが表示されるはずです。右のペインに以下の JSON データをそのまま貼り付けてみてください。

```
{"type": "modal", "callback_id": "page2_modal_submission", "title": {"type": "plain_text", "text": "\u30bf\u30b9\u30af\u306e\u65b0\u898f\u767b\u9332 :pencil:"}, "submit": {"type": "plain_text", "text": "\u9001\u4fe1"}, "close": {"type": "plain_text", "text": "\u30ad\u30e3\u30f3\u30bb\u30eb"}, "blocks": [{"type": "input", "block_id": "title", "element": {"type": "plain_text_input", "action_id": "input", "initial_value": "\u91cd\u8981\u306a\u30bf\u30b9\u30af", "placeholder": {"type": "plain_text", "text": "\u4ef6\u540d\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044"}}, "label": {"type": "plain_text", "text": "\u4ef6\u540d"}, "optional": false}, {"type": "input", "block_id": "assignee", "element": {"type": "users_select", "action_id": "input", "placeholder": {"type": "plain_text", "text": "\u62c5\u5f53\u3059\u308b\u30e6\u30fc\u30b6\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044"}}, "label": {"type": "plain_text", "text": "\u62c5\u5f53\u8005"}, "optional": true}, {"type": "input", "block_id": "priority", "element": {"type": "radio_buttons", "action_id": "input", "initial_option": {"text": {"type": "plain_text", "text": "\u4e2d"}, "value": "m"}, "options": [{"text": {"type": "plain_text", "text": "\u9ad8"}, "value": "h"}, {"text": {"type": "plain_text", "text": "\u4e2d"}, "value": "m"}, {"text": {"type": "plain_text", "text": "\u4f4e"}, "value": "l"}]}, "label": {"type": "plain_text", "text": "\u30d7\u30e9\u30a4\u30aa\u30ea\u30c6\u30a3"}, "optional": false}, {"type": "input", "block_id": "deadline", "element": {"type": "datepicker", "action_id": "input", "initial_date": "2020-10-23", "placeholder": {"type": "plain_text", "text": "\u65e5\u4ed8\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044"}}, "label": {"type": "plain_text", "text": "\u671f\u9650"}, "optional": true}, {"type": "input", "block_id": "description", "element": {"type": "plain_text_input", "action_id": "input", "initial_value": "\u306a\u308b\u65e9\u3067\u304a\u9858\u3044\u3057\u307e\u3059\uff01", "multiline": true, "placeholder": {"type": "plain_text", "text": "\u3067\u304d\u308b\u3060\u3051\u5177\u4f53\u7684\u306b\u8a18\u5165\u3057\u3066\u304f\u3060\u3055\u3044"}}, "label": {"type": "plain_text", "text": "\u8a73\u7d30"}, "optional": true}]}
```

同じ見た目が表示されたはずです。

より詳しく学ぶには、<https://api.slack.com/surfaces/modals/using|ドキュメント（英語）>や <https://api.slack.com/tools/bolt|Bolt のドキュメント>を参照してください。
""",
                ),
            },
        },
    ],
    # --------------------------------------------
    # page 3
    # --------------------------------------------
    [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": i18n("3. External Data Source", "3. 動的なセレクトメニュー"),
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
In this page, you'll learn how to use <https://api.slack.com/reference/block-kit/block-elements#external_multi_select|External Data Source based select menus>. This feature enables developers to build dynamic select menus using any data sources. Your app can easily build "search by keyword" functionalities.

As with the modals in the previous page, your app needs to tell Slack the URL to communicate. Go to *Features* > *Interactivity & Shortcuts* > *Interactivity* and set a URL in the *Select Menus* section. Slack will send requests when a user interacts in select menues and expect your app to return the options as `options` in response body.

Here is a simple demo select menu using external data source.
""",
                    """
このページでは、<https://api.slack.com/reference/block-kit/block-elements#external_multi_select|動的なセレクトメニュー> について説明します。標準のメニューではなく、カスタムで、かつ、入力キーワードに応じた検索結果のような動的な選択肢を返す機能です。

前のページのモーダルと同様、あらかじめ URL を設定しておきます。 *Features* > *Interactivity & Shortcuts* > *Interactivity* のページの最下部に *Select Menus* というセクションがあり、そこに URL を設定します。ここに Slack からリクエストがきたら、決められた形式で選択肢一覧を `options` として応答します。

以下は実際に動作しているデモのセレクトメニューです。
""",
                ),
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n("Search by keyword", "キーワードを入力"),
                    },
                    "min_query_length": 0,
                    "action_id": "external-data-source-example",
                }
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
The <https://api.slack.com/block-kit|*Block Kit*> JSON data for realizing can looks as below. You can go with `multi_external_select` type if you want to enable users to choose multiple items.

```
{
    "type": "external_select",
    "action_id": "demo-selector",
    "placeholder": {"type": "plain_text", "text": "Search by keyword"},
    "min_query_length": 0
}
```

The following server-side code handles the requests for select menu options when a user inputs a keyword.

```
all_options = [
    {"text": {"type": "plain_text", "text": ":cat: Cat"}, "value": "cat",},
    {"text": {"type": "plain_text", "text": ":dog: Dog"}, "value": "dog",},
    {"text": {"type": "plain_text", "text": ":bear: Bear"}, "value": "bear",},
]

@app.options("demo-selector")
def external_data_source_handler(ack, body):
    keyword = body.get("value")
    if keyword is not None and len(keyword) > 0:
        options = [o for o in all_options if keyword in o["text"]["text"]]
        ack(options=options)
    else:
        ack(options=all_options)
```
As you see, the above code has a static array of options. But needless to say, your app can load data from anywhere. Apps can run queries to fetch data in database and/or talk to any backend services. While we used the select menu in Home tabs, the component is available for messages and modals too.

This is a very useful feature for business operations. Make use of it in many situations!
""",
                    """
使用する <https://api.slack.com/block-kit|*Block Kit*> の JSON データは以下の様になります。複数選択にしたい場合は `multi_external_select` にするだけです。

```
{
    "type": "external_select",
    "action_id": "demo-selector",
    "placeholder": {"type": "plain_text", "text": "キーワードを入力"},
    "min_query_length": 0
}
```

ユーザーがキーワードを入力したときに選択肢をロードする処理は以下のように実装できます。

```
all_options = [
    {"text": {"type": "plain_text", "text": ":cat: ねこ"}, "value": "cat",},
    {"text": {"type": "plain_text", "text": ":dog: いぬ"}, "value": "dog",},
    {"text": {"type": "plain_text", "text": ":bear: くま"}, "value": "bear",},
]

@app.options("demo-selector")
def external_data_source_handler(ack, body):
    keyword = body.get("value")
    if keyword is not None and len(keyword) > 0:
        options = [o for o in all_options if keyword in o["text"]["text"]]
        ack(options=options)
    else:
        ack(options=all_options)
```

このサンプル例ではソースコードにデータが直接書かれていますが、もちろんデータベースや他のサービスと連携させることができます。また、ここではホームタブ内に埋め込んでいますが、メッセージやモーダルでも同じように利用することが可能です。

いろんな場面で使える機能なので、ぜひうまく活用してみてください。
""",
                ),
            },
        },
    ],
    # --------------------------------------------
    # page 4
    # --------------------------------------------
    [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": i18n("4. Shortcuts", "4. ショートカット")},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
Let's go to a channel and try shortcuts. As a preparation, you will ask this app to create a test channel for it. Once the channel has been created, you can go to the channel by clicking a link on the modal.
""",
                    """
このページでは、チャンネルに移動して、ショートカットを実行してみましょう。まずは、準備のためにこのアプリにチャンネルをつくらせます。作成後、リンクをクリックしてそのままチャンネルに移動できます。
""",
                ),
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": i18n("Create a test channel", "テスト用チャンネルをつくる"),
                    },
                    "value": "clicked",
                    "style": "primary",
                    "action_id": "page4_create_channel",
                },
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
By the way, the modal starting from the above button utilizes a few Web APIs. For channel creation,  it uses <https://api.slack.com/methods/conversations.create|conversations.create> API method. Then, it invites you to the created channel by <https://api.slack.com/methods/conversations.invite|conversations.invite> API method.

Also, this app subscribes <https://api.slack.com/events/channel_created|channel_created> event in <https://api.slack.com/events-api|Events API>. When a channel is created, this app checks if the channel was created by itself and if so, the app sends a welcome message in this channel.
""",
                    """
ちなみに、上のボタンからの処理がやっていることを簡単に説明しておきます。チャンネルの作成には <https://api.slack.com/methods/conversations.create|conversations.create> という API を使っています。そして、あなたを <https://api.slack.com/methods/conversations.invite|conversations.invite> API を使って作られたチャンネルに招待しています。

それに加えて <https://api.slack.com/events/channel_created|channel_created> というイベントを <https://api.slack.com/events-api|Events API> を使って購読しています。チャンネルが作成されたら、このアプリ自身が作成したチャンネルであるかをチェックした上でウェルカムメッセージを投稿する、ということを行っています。
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
                    """
Welcome back! As we saw in the channel, there are two types of shortcuts. You can choose a right one depending on the situation.

*Global Shortcuts*

You can find the list of global shortcuts from the :zap: icon menu in text composer. It's also possible to search by keyword in the search bar at the top of Slack UI.

*Message Shortcuts*

You can use this type of shortcuts from message menu. If you don't see the one at the three shortcuts, click "More message shortcuts" and find the one you want to use in the whole list.
""",
                    """
おかえりなさい。チャンネルで試したように、ショートカットには以下の二種類があります。用途に合わせて使い分けてみてください。

*グローバルショートカット*

メッセージ入力エリアに :zap: のようなアイコンがあると思いますが、これはクリックするとショートカット一覧が表示されるメニューです。そこから選択してクリックします。検索バーから名前で探して起動することもできます。

*メッセージショートカット*

メッセージのメニューから起動できます。表示されていない場合は「その他のメッセージのショートカット」をクリックして、一覧から検索します。
""",
                ),
            },
        },
    ],
    # --------------------------------------------
    # page 5
    # --------------------------------------------
    [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": i18n("5. Paid Plan Features", "5. 有料プラン向け機能での開発"),
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
In this page, we will learn the features that are available only for paid plan workspaces.

*Steps from Apps*

<https://slack.com/help/articles/360035692513-Guide-to-Workflow-Builder|Workflow Builder> is available for all paid plans. Workflows are useful for automating many operations and/or defining input data formats in various situations.

A workflow consists of a single trigger and multiple steps. Users can use not only built-in steps (Send a message, Create a form) but also custom steps. To build your own custom steps, refer to the <https://api.slack.com/workflows/steps|developer guide> and <https://api.slack.com/tutorials/workflow-builder-steps|tutorial>. <https://api.slack.com/tools/bolt|Bolt farmework> should make the development much easier.

<https://my.slack.com/apps/collection/workflows|The collection page in App Directory> is a good place to find public apps that already support custom steps. You can try them out just by installing the apps.

*Admin Web API*

Among the Web APIs that are available at <https://api.slack.com/methods|api.slack.com/methods>, the ones having the admin. prefix are available for Enterprise Grid admin users. Organization admins can use the admin.* APIs with their user tokens for running management operations via APIs.

*SCIM API*

<http://www.simplecloud.info/|SCIM (System for Cross-domain Identity Management)> is a public specification that is supported by many services. <https://api.slack.com/scim|SCIM API> is available for Plus with SSO and Enterprise Grid plans.

*Audit Logs API*

<https://api.slack.com/admins/audit-logs|Audit Logs API> is available for monitoring various audit events in an Enterprise Grid organization. See the <https://api.slack.com/admins/audit-logs|document> to learn how to use it.

*Discovery API*

On the Enterprise Grid plan, Org Owners can export data using Slack's <https://slack.com/help/articles/360002079527-A-guide-to-Slacks-Discovery-APIs|Discovery API>. 
""",
                    """
このページでは有料プランのワークスペースでのみ利用可能な機能を用いた開発についてご紹介します。

*ワークフローのカスタムステップ*

<https://slack.com/intl/ja-jp/help/articles/360035692513|ワークフロービルダー>は、全ての有料プランで利用可能な機能です。定型処理を自動化したり、フォームを使って入力内容のルールを定めることができます。

ワークフローは、一つのトリガーと複数のステップで構成されますが、このステップにカスタム開発したものを組み込むことができます。開発手順は、<https://api.slack.com/workflows/steps|開発者向けドキュメント>、<https://api.slack.com/tutorials/workflow-builder-steps|チュートリアル>を参考にしてください。<https://api.slack.com/tools/bolt|Bolt フレームワーク>を使うと、楽に開発できます。 

<https://my.slack.com/apps/collection/workflows|こちらのページ>で紹介されている通り、既に多くのアプリがこのワークフローステップを提供しており、ワークフロービルダーでワークフローをつくるときにそれらを組み込むことができます。

*管理系 (admin) Web API*

<https://api.slack.com/methods|api.slack.com/methods> で公開されている API のうち admin. というネームスペースから始まる Web API は全て Enterprise Grid プランでのみ利用可能です。

オーガナイゼーションの管理者が admin.* API を使うアプリを自分のユーザートークンで利用することで、様々な管理系のオペレーションを API 経由で実行することができます。

*SCIM API*

<http://www.simplecloud.info/|SCIM (System for Cross-domain Identity Management)> は、数多くのサービスでサポートされている仕様です。SSO （シングルサインオン）を有効にしている Plus または Enterprise Grid プランでは、<https://api.slack.com/scim|SCIM API> を利用することができます。

*Audit Logs API*

<https://api.slack.com/admins/audit-logs|Audit Logs API> は Enterprise Grid のオーガナイゼーション内で発生したイベントをモニタリングするための API 群です。実際の利用方法は <https://api.slack.com/admins/audit-logs|こちらのドキュメント>を参考にしてください。

*Discovery API*

<https://slack.com/intl/ja-jp/help/articles/360002079527|Discovery API> は、Slack のお客様が選んだパートナーと Enterprise Grid のオーガナイゼーションをつなぐための API です。この API を有効にすることで、対応したソリューションと連携したり、カスタムのアプリケーションを開発することができます。
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
                    """
Developers acn submit a request to use sandbox environment for Enterprise Grid ready Slack app development.

Refer to the <https://api.slack.com/enterprise/grid/testing|testing guide> for details.
    """,
                    """
Enterprise Grid に対応した Slack アプリの開発を行う開発者はサンドボックス環境を申請することができます。

<https://api.slack.com/enterprise/grid/testing|こちらのガイド>を参考にしてみてください。
    """,
                ),
            },
        },
    ],
    # --------------------------------------------
    # page 6
    # --------------------------------------------
    [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": i18n("6. Further information", "6. インタラクティブなアプリをつくるための情報リソース"),
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": i18n(
                    """
Lastly, here are helpful resource to learn further about interactive features in the Slack Platform:

• <https://api.slack.com/|Slack Platform API Ddocuments>
• <https://medium.com/slack-developer-blog|Slack Platform Blog>
• <https://api.slack.com/changelog|Recent changes to the Slack platform>

This app is built with <https://slack.dev/bolt-python/|Bolt for Python>. We highly recommend using Bolt for building interactive Slack apps.
• <https://api.slack.com/tools/bolt|Bolt Framework (JavaScript, Python, Java)>

Here are the documents of the features covered by this tutorial.

• <https://api.slack.com/methods|Web API>
• <https://api.slack.com/surfaces/tabs|Home Tab>
• <https://api.slack.com/surfaces/modals|Modals>
• <https://api.slack.com/messaging/composing|Messaging>
• <https://api.slack.com/events-api|Events API>
• <https://api.slack.com/events|Events>

2,200+ apps are listed in <https://my.slack.com/apps|App Directory>. Learning from popular apps is a great way to learn best practices.

Join the open developer community: <https://join.slack.com/t/community/shared_invite/enQtNzYxNzM5NzU0Mzg3LWFhZjE3ZjY1M2JhM2MzNGNmMmE0Zjc4Y2E5NDc2NGJiODAxNDMzN2Y1MjVlYWU3ZGVlYzhlMDVhNzA0Nzg1OGY|Slack Community Workspace> and <https://slackcommunity.com/|Slack Platform Community Website>


Thanks a lot for completing this tutorial! Enjoy Slack app development :wave:
        """,
                    """
最後に、このチュートリアルで紹介したインタラクティブな機能を使ったアプリの開発をさらに深く学んでいくために有益なリソースの一覧を紹介しておきます。

• <https://api.slack.com/|Slack プラットフォームドキュメントのトップページ>
• <https://medium.com/slack-developer-blog|Slack プラットフォームの公式ブログ>
• <https://api.slack.com/changelog|Slack プラットフォームの更新履歴>

このアプリも <https://slack.dev/bolt-python/|Bolt for Python> で実装されていますが、インタラクティブな機能を実装するには Bolt を使うことをおすすめします。
• <https://api.slack.com/tools/bolt|Bolt フレームワークの一覧>

このチュートリアルでご紹介した各機能のドキュメントページです。

• <https://api.slack.com/methods|Web API の一覧>
• <https://api.slack.com/surfaces/tabs|ホームタブ>
• <https://api.slack.com/surfaces/modals|モーダル>
• <https://api.slack.com/messaging/composing|メッセージの作成>
• <https://api.slack.com/events-api|イベント API>
• <https://api.slack.com/events|イベントの一覧>

上記はすべて英語ですが、一部は日本語にも翻訳されています。

• <https://api.slack.com/lang/ja-jp|日本語ドキュメントの一覧>
• <https://qiita.com/organizations/slack|Qiita 掲載の記事>
• <https://slack.dev/bolt-js/ja-jp/tutorial/getting-started|Bolt for JavaScript>, <https://slack.dev/java-slack-sdk/guides/ja/|Bolt for Java>

<https://my.slack.com/apps|App Directory> には 2,200 以上のアプリが公開されています。ベストプラクティスを知るには、人気のあるアプリがどのような挙動になっているかを研究してみるのもおすすめです。

オープンな開発者コミュニティもあります。<https://join.slack.com/t/community/shared_invite/enQtNzYxNzM5NzU0Mzg3LWFhZjE3ZjY1M2JhM2MzNGNmMmE0Zjc4Y2E5NDc2NGJiODAxNDMzN2Y1MjVlYWU3ZGVlYzhlMDVhNzA0Nzg1OGY|Slack ワークスペース>と<https://slackcommunity.com/|コミュニティサイト>にアクセスしてみてください。


最後までお疲れ様でした！

Slack プラットフォームの機能を活用して、素晴らしいアプリを開発してください :wave:
        """,
                ),
            },
        },
    ],
]


# --------------------------------------------
# Home tab loading
# --------------------------------------------


def build_pager_block(page: int) -> dict:
    pager_block_elements = []
    if page <= 1:
        pager_block_elements = [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": i18n("Next", "次へ")},
                "value": "2",
                "action_id": "tutorial_page_transition_2",
            }
        ]
    elif page >= len(pages):
        pager_block_elements = [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": i18n("Previous", "前へ")},
                "value": f"{page - 1}",
                "action_id": f"tutorial_page_transition_{page - 1}",
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": i18n("First Page", "最初のページへ")},
                "value": "1",
                "action_id": f"tutorial_page_transition_0",
            },
        ]
    else:
        pager_block_elements = [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": i18n("Previous", "前へ")},
                "value": f"{page - 1}",
                "action_id": f"tutorial_page_transition_{page - 1}",
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": i18n("Next", "次へ")},
                "value": f"{page + 1}",
                "action_id": f"tutorial_page_transition_{page + 1}",
            },
        ]
    return {"type": "actions", "elements": pager_block_elements}


def tutorial_view(page: int) -> dict:
    page_content = []
    if page <= len(pages):
        page_content = pages[page - 1]

    tz = datetime.timezone(datetime.timedelta(hours=+9), "JST")
    now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    blocks = page_content + [
        {"type": "divider"},
        build_pager_block(page),
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": i18n(f"Last Updated: {now}, JST", f"最終更新日時: {now}, JST"),
                }
            ],
        },
    ]
    return {"type": "home", "blocks": blocks}


def app_home_opened():
    pass


def app_home_opened_lazy(event, context: BoltContext, client: WebClient):
    if event["tab"] == "home":
        client.views_publish(user_id=context.user_id, view=tutorial_view(1))


def tutorial_page_transition(ack):
    ack()


def tutorial_page_transition_lazy(
    action: dict, context: BoltContext, client: WebClient
):
    client.views_publish(
        user_id=context.user_id, view=tutorial_view(int(action["value"]))
    )


# --------------------------------------------
# page 1
# --------------------------------------------


def page1_home_tab_button_click(ack):
    ack()


def page1_home_tab_button_click_lazy(action: dict, body: dict, client: WebClient):
    num = int(action["value"])
    message = i18n(
        f"""
You've got {':star:' * num}!

The button was configured as below. By setting a unique string (action_id) such as "page1_home_tab_button_{num}", Slack Platform can distinguish each button from others.

Your app receives an associated value ("{num}" in this case) to the clicked button in a sent payload from Slack. Using the ID of the selected entity is a common practice.

```
{{
    "type": "actions",
    "elements": [
        {{
            "type": "button",
            "text": {{
                "type": "plain_text",
                "text": "{':star:' * num}"
            }},
            "value": "{num}",
            "action_id": "page1_home_tab_button_{num}"
        }}
    ]
}}
```
    """,
        f"""
:star: {num} つを選択しましたね :wave:

ボタンは以下の様に設定されています。ボタンに "page1_home_tab_button_{num}" のような ID をふっておくことで、他のボタンと区別することができます。

そして Slack からのペイロードにはその ID と紐づく形で UI には表示されていない　"{num}" という値を受け取ることができます。ここには選択された対象の ID などを設定しておくとよいでしょう。

```
{{
    "type": "actions",
    "elements": [
        {{
            "type": "button",
            "text": {{
                "type": "plain_text",
                "text": "{':star:' * num}"
            }},
            "value": "{num}",
            "action_id": "page1_home_tab_button_{num}"
        }}
    ]
}}
```
    """,
    )
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": i18n("Demo App", "デモアプリ")},
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": message}}
            ],
        },
    )


def page1_home_tab_users_select(ack):
    ack()


def page1_home_tab_users_select_lazy(action, body: dict, client: WebClient):
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": i18n("Demo App", "デモアプリ")},
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n(
                            f"You selected <@{action['selected_user']}>!",
                            f"あなたは <@{action['selected_user']}> を選択しました！",
                        ),
                    },
                }
            ],
        },
    )


# --------------------------------------------
# page 2
# --------------------------------------------


def page2_modal(ack):
    ack()


def page2_modal_lazy(body: dict, client: WebClient, logger: Logger):
    modal = {
        "type": "modal",
        "callback_id": "page2_modal_submission",
        "title": {
            "type": "plain_text",
            "text": i18n("New Task :pencil:", "タスクの新規登録 :pencil:"),
        },
        "submit": {"type": "plain_text", "text": i18n("Submit", "送信")},
        "close": {"type": "plain_text", "text": i18n("Cancel", "キャンセル")},
        "blocks": [
            {
                "type": "input",
                "block_id": "title",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "input",
                    "initial_value": i18n("Help!", "重要なタスク"),
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n("Write the title", "件名を入力してください"),
                    },
                },
                "label": {"type": "plain_text", "text": i18n("Title", "件名")},
                "optional": False,
            },
            {
                "type": "input",
                "block_id": "assignee",
                "element": {
                    "type": "users_select",
                    "action_id": "input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n("Select an assignee", "担当するユーザを選択してください"),
                    },
                },
                "label": {"type": "plain_text", "text": i18n("Assignee", "担当者")},
                "optional": True,
            },
            {
                "type": "input",
                "block_id": "priority",
                "element": {
                    "type": "radio_buttons",
                    "action_id": "input",
                    "initial_option": {
                        "text": {"type": "plain_text", "text": i18n("Medium", "中")},
                        "value": "m",
                    },
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": i18n("High", "高")},
                            "value": "h",
                        },
                        {
                            "text": {"type": "plain_text", "text": i18n("Medium", "中")},
                            "value": "m",
                        },
                        {
                            "text": {"type": "plain_text", "text": i18n("Low", "低")},
                            "value": "l",
                        },
                    ],
                },
                "label": {"type": "plain_text", "text": i18n("Priority", "プライオリティ")},
                "optional": False,
            },
            {
                "type": "input",
                "block_id": "deadline",
                "element": {
                    "type": "datepicker",
                    "action_id": "input",
                    "initial_date": datetime.datetime.today().strftime("%Y-%m-%d"),
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n("Select the due date", "日付を選択してください"),
                    },
                },
                "label": {"type": "plain_text", "text": i18n("Due Date", "期限")},
                "optional": True,
            },
            {
                "type": "input",
                "block_id": "description",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "input",
                    "initial_value": i18n("ASAP!", "なる早でお願いします！"),
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n(
                            "Write details as much as possible", "できるだけ具体的に記入してください"
                        ),
                    },
                },
                "label": {"type": "plain_text", "text": i18n("Description", "詳細")},
                "optional": True,
            },
        ],
    }
    logger.info(json.dumps(modal))
    client.views_open(trigger_id=body["trigger_id"], view=modal)


def page2_modal_submission(ack: Ack, view: dict):
    values = view.get("state", {}).get("values", {})
    title = values.get("title", {}).get("input", {}).get("value")
    assignee = values.get("assignee", {}).get("input", {}).get("selected_user")
    priority = (
        values.get("priority", {})
        .get("input", {})
        .get("selected_option", {})
        .get("text", {})
        .get("text")
    )
    deadline = values.get("deadline", {}).get("input", {}).get("selected_date")
    description = values.get("description", {}).get("input", {}).get("value")

    errors = {}
    if len(title) < 8:
        errors["title"] = i18n(
            "Title must contain at least 8 characters", "件名は 8 文字以上で入力してください"
        )
    if (
        deadline is not None
        and datetime.datetime.strptime(deadline, "%Y-%m-%d")
        <= datetime.datetime.today()
    ):
        errors["deadline"] = i18n("Due Date must be in the future", "期限は明日以降を指定してください")
    if description is not None and len(description) < 20:
        errors["description"] = i18n(
            "Description must contain at least 20 characters", "詳細は 20 文字以上で入力してください"
        )

    if len(errors) > 0:
        return ack(response_action="errors", errors=errors)

    ack(
        response_action="update",
        view={
            "type": "modal",
            "callback_id": "page2_modal_submission_result",
            "title": {"type": "plain_text", "text": i18n("Accepted!", "タスク登録完了")},
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": i18n(f"Title: {title or ''}", f"件名: {title or ''}"),
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": i18n(
                                f"Assignee: {f'<@{assignee}>' if assignee else 'TBD'}",
                                f"担当者: {f'<@{assignee}>' if assignee else '未定'}",
                            ),
                        },
                        {
                            "type": "plain_text",
                            "text": i18n(
                                f"Priority: {priority or ''}",
                                f"プライオリティ: {priority or ''}",
                            ),
                        },
                        {
                            "type": "plain_text",
                            "text": i18n(
                                f"Due Date: {deadline or ''}", f"期限: {deadline or ''}"
                            ),
                        },
                        {
                            "type": "plain_text",
                            "text": i18n(
                                f"Description: {description or ''}",
                                f"詳細: {description or ''}",
                            ),
                        },
                    ],
                },
            ],
        },
    )


# --------------------------------------------
# page 3
# --------------------------------------------

all_options = [
    {
        "text": {"type": "plain_text", "text": i18n(":cat: Cat", ":cat: ねこ")},
        "value": "cat",
    },
    {
        "text": {"type": "plain_text", "text": i18n(":dog: Dog", ":dog: いぬ")},
        "value": "dog",
    },
    {
        "text": {"type": "plain_text", "text": i18n(":bear: Bear", ":bear: くま")},
        "value": "bear",
    },
]


def external_data_source_handler(ack: Ack, body: dict):
    keyword = body.get("value")
    if keyword is not None and len(keyword) > 0:
        options = [o for o in all_options if keyword in o["text"]["text"]]
        ack(options=options)
    else:
        ack(options=all_options)


# --------------------------------------------
# page 4
# --------------------------------------------


def page4_create_channel(ack):
    ack()


def page4_create_channel_lazy(
    body: dict, context: BoltContext, client: WebClient, logger: Logger
):
    modal = {
        "type": "modal",
        "callback_id": "page4_create_channel_submission",
        "title": {
            "type": "plain_text",
            "text": i18n("New Channel :pencil:", "チャンネル作成 :pencil:"),
        },
        "submit": {"type": "plain_text", "text": i18n("Submit", "実行")},
        "close": {"type": "plain_text", "text": i18n("Cancel", "キャンセル")},
        "blocks": [
            {
                "type": "input",
                "block_id": "channel_name",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "input",
                    "initial_value": i18n(
                        f"_learning-app-{context.user_id.lower()}",
                        f"_学習用チャンネル-{context.user_id.lower()}",
                    ),
                    "placeholder": {
                        "type": "plain_text",
                        "text": i18n("Set the channel name", "チャンネル名を入力してください"),
                    },
                },
                "label": {"type": "plain_text", "text": i18n("Channel Name", "チャンネル名")},
                "optional": False,
            },
        ],
    }
    logger.info(json.dumps(modal))
    client.views_open(trigger_id=body["trigger_id"], view=modal)


def page4_create_channel_submission(ack: Ack):
    ack(
        response_action="update",
        view={
            "type": "modal",
            "callback_id": "page4_create_channel_submission",
            "title": {
                "type": "plain_text",
                "text": i18n("Creating a channel", "チャンネル作成中"),
            },
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n("Wait a second... :zzz:", "少々お待ちください... :zzz:"),
                    },
                },
            ],
        },
    )


def page4_create_channel_submission_lazy(
    view: dict, context: BoltContext, client: WebClient
):
    values = view.get("state", {}).get("values", {})
    channel_name = values.get("channel_name", {}).get("input", {}).get("value")
    channel_id = ""
    try:
        channel_creation = client.conversations_create(name=channel_name)
        channel_id = channel_creation["channel"]["id"]
        client.conversations_join(channel=channel_id)
        client.conversations_invite(channel=channel_id, users=[context.user_id])
    except SlackApiError as e:
        error = e.response["error"]
        error_message = i18n(
            f"The app failed to create a channel ({error}) :bow:",
            f"チャンネル作成中にエラーが発生しました ({error}) :bow:",
        )
        if error == "name_taken":
            error_message = i18n(
                f"The channel already exists :bow:", f"このチャンネル名はすでに存在しています :bow:"
            )
        elif error == "invalid_name_specials":
            error_message = i18n(
                f"Unfortunately, you cannot use special characters or upper case characters for channel names :bow:",
                f"チャンネル名にアルファベット大文字や特殊文字などは使えません :bow:",
            )
        client.views_update(
            view_id=view["id"],
            view={
                "type": "modal",
                "callback_id": "page2_modal_submission_result",
                "title": {
                    "type": "plain_text",
                    "text": i18n("Channel Creation Failure", "チャンネル作成エラー"),
                },
                "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": error_message},
                    }
                ],
            },
        )
        return

    client.views_update(
        view_id=view["id"],
        view={
            "type": "modal",
            "callback_id": "page2_modal_submission_result",
            "title": {
                "type": "plain_text",
                "text": i18n("Channel Created!", "チャンネル作成完了"),
            },
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n(
                            "The app successfully created the channel!", "チャンネルを作成しました！"
                        ),
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n(
                            f"Go to <#{channel_id}> and follow the instructions.",
                            f"<#{channel_id}> へ移動してそこで指示に従ってショートカットを実行してみてください。",
                        ),
                    },
                },
            ],
        },
    )


def page4_create_channel_setup(ack):
    ack()


def page4_create_channel_setup_lazy(
    event: dict, context: BoltContext, client: WebClient
):
    creator = event["channel"]["creator"]
    if creator == context.bot_user_id:
        client.chat_postMessage(
            channel=event["channel"]["id"],
            text=i18n(
                "Welcome to this test channel! Let's try shortcuts.",
                "ようこそ、テスト用チャンネルへ！ここではショートカットを試してみましょう。",
            ),
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n(
                            """
Welcome to this test channel! Let's try shortcuts.

You can find the list of global shortcuts from the :zap: icon menu in text composer. It is a menu to display the list of available global shortcuts.

Once the menu opens, search by "Learn". You will find the "Learn Global Shortcut". Let's click the one!
                            """,
                            """
ようこそ、テスト用チャンネルへ！ここではショートカットを試してみましょう。

メッセージ入力エリアに :zap: のようなアイコンがあると思いますが、これはクリックするとショートカット一覧が表示されるメニューです。

メニューが開いたら「学習」で検索してみてください。そうすると「学習用のグローバルショートカット」というものが見つかるはずです。それをクリックしてみましょう。
                            """,
                        ),
                    },
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": i18n("Shortcut Menu", "ショートカットメニュー"),
                    },
                    "image_url": i18n(
                        "https://user-images.githubusercontent.com/19658/97389676-40b13280-191e-11eb-859a-1834ee83497c.png",
                        "https://user-images.githubusercontent.com/19658/96969620-a92e9700-154d-11eb-9fa0-97ee7644a82f.png"
                    ),
                    "alt_text": i18n("Shortcut Menu", "ショートカットメニュー"),
                },
            ],
        )


def global_shortcut_handler(ack: Ack, body: dict, client: WebClient):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "global-shortcut-example_submission",
            "title": {"type": "plain_text", "text": i18n("Global Shortcuts", "グローバルショートカット")},
            "submit": {"type": "plain_text", "text": i18n("Submit", "送信")},
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n(
                            """
This Slack app opened this modal in response to your global shortcut invocation.

You can use global shortcuts from the search bear. Thus, the current channel may not exist in some cases. If your app needs to notify users in a channel when the process completes, the app can use an input block along with `default_to_current_conversation` option. Here is an example:
                            """,
                            """
グローバルショートカットからこのモーダルを起動しました。

グローバルショートカットは検索バーからも実行できます。そのため、必ずしも「現在のチャンネル」が存在するとは限りません。完了後に何か通知したいという場合は `default_to_current_conversation` というオプションを指定したセレクトメニューを使用します。以下がその例です。
                            """
                        ),
                    },
                },
                {
                    "type": "input",
                    "block_id": "channel",
                    "element": {
                        "type": "conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": i18n("Unset if not in channel", "チャンネル外で起動したときは未設定"),
                        },
                        "default_to_current_conversation": True,
                        "action_id": "input",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": i18n("Current Channel", "起動したチャンネル"),
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n("""
If you clicked this shortcut in a channel, the channel should be selected in the above select menu. As this app does, making the input block required is a good way to surely ask end users to tell the place to notify.

The following Python code is a simple listener that handles global shortcut requests.

```
@app.shortcut("the callback_id you set when creating a shortcut")
def handler(ack, body, client):
    # Send 200 OK
    ack()

    # Open a modal via views.open API
    client.views_open(
        # Modals require trigger_id
        trigger_id=body["trigger_id"],
        # Build a modal view
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Title"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [...]
        },
    )
```

That's it. To go to the next, submit this modal now!
""",
"""
このショートカットをチャンネルから起動したのであれば、選択状態になっているはずです。このように必須の入力項目にしておけば、チャンネル以外から起動された場合にも通知先のチャンネルを選ぶように強制することができます。
グローバルショートカットをハンドリングする Python のコードは以下のようになります。
```
@app.shortcut("ショートカット作成時に指定した callback_id")
def handler(ack, body, client):
    # リクエストに対して 200 OK を返す
    ack()
    # views.open API を使ってモーダルを開く
    client.views_open(
        # ユーザーアクション毎に trigger_id が発行される
        # trigger_id なしでモーダルは起動できない
        trigger_id=body["trigger_id"],
        # モーダルの view を組み立てて渡す
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "タイトル"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [...]
        },
    )
```
それでは、このモーダルをこのまま送信してみてください。
"""
),
                    },
                },
            ],
        },
    )


def global_shortcut_view_submission(ack):
    ack()


def global_shortcut_view_submission_lazy(view: dict, client: WebClient):
    client.chat_postMessage(
        channel=view["state"]["values"]["channel"]["input"]["selected_conversation"],
        text=i18n(
            """Let's try message shortcuts. You can start a message shortcut from the message menu. If you don't see the shortcut in the menu, click "More message shortcuts..." to access the whole list.""",
            "次はメッセージショートカットを実行してみましょう。以下のようにメッセージメニューから「学習用のメッセージメニュー」を起動してください。表示されていない場合は「その他のメッセージのショートカット」をクリックして、一覧から検索してください。"),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text":i18n(
                        """Let's try message shortcuts. You can start a message shortcut from the message menu. If you don't see the shortcut in the menu, click "More message shortcuts..." to access the whole list.""",
                        "次はメッセージショートカットを実行してみましょう。以下のようにメッセージメニューから「学習用のメッセージメニュー」を起動してください。表示されていない場合は「その他のメッセージのショートカット」をクリックして、一覧から検索してください。"
                    ),
                },
            },
            {
                "type": "image",
                "title": {"type": "plain_text", "text": i18n("Message Menu", "メッセージメニュー")},
                "image_url": "https://user-images.githubusercontent.com/19658/96974266-f44ba880-1553-11eb-94f0-b40408ee0731.gif",
                "alt_text": i18n("Message Menu", "メッセージメニュー"),
            },
        ],
    )


def message_shortcut_handler(ack: Ack):
    ack()


def message_shortcut_handler_lazy(body: dict, context: BoltContext, client: WebClient, logger: Logger):
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "global-shortcut-example_submission",
            "title": {"type": "plain_text", "text": i18n("Message Shortcuts", "メッセージショートカット")},
            "close": {"type": "plain_text", "text": i18n("Close", "閉じる")},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": i18n(
                            """
This Slack app opened this modal in response to your message shortcut invocation. Message shortcuts can be used for creating a task with the message text and user information.

The following Python code is a simple listener that handles message shortcut requests.

```
@app.shortcut("the callback_id you set when creating a shortcut")
def handler(ack, body, client):
    # Send 200 OK
    ack()

    # Open a modal via views.open API
    client.views_open(
        # Modals require trigger_id
        trigger_id=body["trigger_id"],
        # Build a modal view
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Title"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [...]
        },
    )
```
                            """,
                            """
メッセージショートカットからこのモーダルを起動しました。メッセージショートカットのよくある例は、メッセージ本文や投稿者を含めたタスクなどを外部のシステムに登録する連携アプリです。

メッセージショートカットをハンドリングする Python のコードは以下のようになります。

```
@app.shortcut("ショートカット作成時に指定した callback_id")
def handler(ack, body, client):
    # リクエストに対して 200 OK を返す
    ack()

    # views.open API を使ってモーダルを開く
    client.views_open(
        # ユーザーアクション毎に trigger_id が発行される
        # trigger_id なしでモーダルは起動できない
        trigger_id=body["trigger_id"],
        # モーダルの view を組み立てて渡す
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "タイトル"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [...]
        },
    )
```

ワークフロービルダーのリアクションをトリガーを使って似たような処理を実装できますが、メッセージショートカットを実装すると、より使い勝手の良いものを実装できるでしょう。
                            """
                        ),
                    },
                },
            ],
        },
    )
    try:
        team_id = context.team_id
        # https://github.com/slackapi/bolt-python/pull/126
        app_id = client.bots_info(bot=context.bot_id)["bot"]["app_id"]
        client.chat_postMessage(
            channel=body["channel"]["id"],
            text=i18n(
                f"We've learnt how to run two types of shortcuts. Go back to <slack://app?team={team_id}&id={app_id}&tab=home|Home tab> and continue learning more features!",
                f"ここでは、二種類のショートカットの実行を学びました。<slack://app?team={team_id}&id={app_id}&tab=home|ホームタブに戻って>、学習の続きをみていきましょう。"
            ),
        )
    except Exception as e:
        logger.exception(f"Failed to post a message: {e}")

# --------------------------------------------
# page 5
# --------------------------------------------

# --------------------------------------------
# page 6
# --------------------------------------------
