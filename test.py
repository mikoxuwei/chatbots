from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json

# 如果你有用 .env 可以用 dotenv 載入
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

# 移到全域變數
access_token = "LINE_CHANNEL_ACCESS_TOKEN"
secret = "LINE_CHANNEL_SECRET"
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

@app.route("/", methods=["POST"])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print("Received body:", body)  # debug 印出 webhook payload

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print("User said:", msg)  # debug 看有沒有成功收到文字

    reply = f"你說了：{msg}"  # 測試先回傳一樣的內容

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
