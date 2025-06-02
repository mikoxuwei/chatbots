from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from gemini_api import get_gemini_reply
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
# === 把這兩行換成你自己的 ===
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    print("收到 webhook:", body)  # debug 用
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_msg = event.message.text
#     print("使用者說：", user_msg)

#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=f"你說了：「{user_msg}」")
#     )

# 設定 API 金鑰
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# 使用正式 API v1 和 gemini-1.5-pro 模型（新版且穩定）
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

def get_gemini_reply(user_input):
    response = model.generate_content(user_input)
    return response.text

# 載入 FAQ
with open("faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()
    reply = None

    # FAQ 匹配（簡單關鍵字比對）
    for keyword in faq_data:
        if keyword in user_msg:
            reply = faq_data[keyword]
            break

    # 若無匹配，改用 Gemini 回覆（待接）
    if not reply:
        reply = get_gemini_reply(user_msg)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


if __name__ == "__main__":
    app.run(port=5000)