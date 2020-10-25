## Slack アプリ開発体験アプリ

### すぐに試すことができます

https://j.mp/slack-dev からインストールできます。開発用のワークスペースなどにインストールして試してみてください。

<img width="600" src="https://user-images.githubusercontent.com/19658/97100273-33edce00-16d5-11eb-87d0-11eb0e205417.png">

<img width="600" src="https://user-images.githubusercontent.com/19658/97100270-2fc1b080-16d5-11eb-8b17-bcc5ae86a7db.png">

### Slack アプリの設定方法

全ての機能を動作させるためには Slack アプリの設定は以下の通り行う必要があります。https://api.slack.com/apps からアプリを作成、以下の設定を行ってください。末尾にある AWS API Gateway + Lambda へのデプロイ手順を使った場合は Request URL は `https://{xxx}.execute-api.ap-northeast-1.amazonaws.com/default/slack_learning_app_ja` のようになるはずです。

#### Features > App Home

* Show Tabs > Home Tab が有効になっている
* Show Tabs > Messages Tab が有効になっている

#### Features > Interactivity & Shortcuts

* Interactivity が有効になっている
* Request URL が正しく設定されている
* Shortcuts に以下の二つ追加されている
  * グローバルショートカット（Callback ID `global-shortcut-example`）
  * メッセージショートカット（Callback ID `message-shortcut-example`）
* Select Menus に Request URL と同じ URL が設定されている

#### Features > OAuth & Permissions

* Redirect URLs に Request URL と同じ URL を設定している
* Scopes の Bot Token Scopes に以下が設定されている
  * channels:join
  * channels:manage
  * channels:read
  * chat:write
  * chat:write.public
  * commands
  * im:write
  * users:read

#### Features > Event Subscriptions

ここでの Request URL の設定時には、その URL が応答を返せる状態になっている必要があります。

* Enable Events が有効になっている
* Request URL が正しく設定されている
* Subscribe to bot events で以下のイベントが設定されている
  * app_home_opened
  * channel_created

### デプロイ

### Heroku などにデプロイする

連携するデータストアなどを適切に設定した後、[対応している Web フレームワーク](https://github.com/slackapi/bolt-python/tree/main/examples)で動かすことができます。

### AWS API Gateway + Lambda にデプロイする方法（一例）

以下は python-lambda というツールを使った設定の手順例です。別のツールを使えば、このような手順でやる必要はありません。

```bash
cp _env .env

#
# .env を適切に設定する
#

# .env の内容を読み込む
source .env

#
# lambda_config.yaml で指定されている IAM Role を作る
#
export policy_name=slack_dev_learning_app_policy
aws iam create-policy \
  --policy-name ${policy_name} \
  --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["lambda:InvokeFunction"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:ReplicateObject",
        "s3:DeleteObject"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}'
export account_id=`aws sts get-caller-identity | jq .Account | awk -F\" '{print $2}'`
export policy_arn=arn:aws:iam::${account_id}:policy/slack_dev_learning_app_policy

export role_name=slack_dev_learning_app_role
aws iam create-role \
  --role-name ${role_name} \
  --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": ["lambda.amazonaws.com"] },
      "Action": ["sts:AssumeRole"]
    }
  ]
}
'
aws iam attach-role-policy \
  --role-name ${role_name} \
  --policy-arn ${policy_arn}

#
# Lambda 関数を作成してデプロイする
#
pip install python-lambda
lambda deploy --config-file lambda_config.yaml --requirements requirements.txt

#
# API Gateway は管理コンソールから設定してください
#
# なお、Event Subscriptions の Request URL 設定は
# URL が正しく動作しているかを検証するため、ここまで完了してからでないと設定できません
#
```
