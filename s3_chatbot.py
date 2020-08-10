from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# 引入之前boto3，執行AWS CLI 建立隱藏檔，不將重要資料上傳
import boto3
s3_client = boto3.client(
    's3'
)


app = Flask(__name__)

# 引入line token
import _tok
line_bot_api = LineBotApi(_tok.tok()['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(_tok.tok()['YOUR_CHANNEL_SECRET'])




@app.route("/callback", methods=['POST'])
def callback():   

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # 紀錄用戶log
    with open('event.log','w',encoding='utf8') as f:
        f.write(body+'\r')


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))



'''

當handler收到用戶傳來的訊息事件，且為圖片消息

請line_bot_api 把圖片從line抓回來，儲存到本地端
請line_bot_api 回復用戶，說圖片以儲存

請s3_client上傳到s3的bucket(iii-tutorial-v2)，指定資料夾(student21)
    準備好 s3_client (寫至全域環境內)
    使用s3_client上傳至桶子內


'''

from linebot.models import ImageMessage
@handler.add(MessageEvent,message=ImageMessage)
def handle_image_message(event):

    # 請line_bot_api 把圖片從line抓回來，儲存本地端
    # 圖片名字以消息id做命名
    # line_bot_api get message content line-bot-sdk
    # google~


    message_content = line_bot_api.get_message_content(event.message.id)
    file_name = event.message.id + '.jpg'

    with open(file_name, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)


    # 請line_bot_api 回復用戶，說圖片以儲存
    # line_bot_api reply TextSendMessage
    line_bot_api.reply_message(
        event.reply_token,
        [
         TextSendMessage(text="圖片已儲存，檔案為" + file_name),
         TextSendMessage(text="user1 : 你在說啥"),
         TextSendMessage(text="user2 : 閉嘴"),
         TextSendMessage(text="user3 : zzzzzz"),
         TextSendMessage(text="user3 : 哈欠~"),
        ]
    )

    # 使用s3_client上傳至桶子內(iii-tutorial-v2)內的指定資料夾
    s3_client.upload_file(file_name, 'iii-tutorial-v2', 'student21/'+file_name)

    # 把圖片上船者的信息，圖片位置在哪，插入資料庫，圖書館索引，google，sheet



if __name__ == "__main__":
    app.run()