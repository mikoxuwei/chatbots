
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import google.generativeai as genai
import os, json

# === 環境設定 ===
load_dotenv()
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# === Gemini 設定 ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# === FAQ 載入 ===
with open("faq2.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)["faq"]

# Gemini 回覆封裝
def get_semantic_faq_or_reply(user_input):
    try:
        faq_text_block = "\n".join([f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}" for i, item in enumerate(faq_data)])
        prompt = f"""
            你是「毛起來找家」的專業客服人員。請根據以下 FAQ 判斷使用者的問題是否已被涵蓋，並直接回覆最適合的答案內容（A#）。
            若 FAQ 沒有涵蓋，請根據下方限制，自行生成一段溫暖、清楚、具體的繁體中文回答。

            請根據提問的主題，**只回答與該問題直接相關的一小段內容**，不需要一次講完所有資訊。

            FAQ：
            {faq_text_block}

            使用者問題如下：
            「{user_input}」

            限制：
            - 僅回答與「領養寵物」、「飼養與照顧」、「常見疾病」、「疫苗與防疫」、「飼主責任」、「寵物用品建議」相關問題
            - 若提到想領養的動物，請建議查看官網資訊
            - 若提到用品，可推薦商品並補充「若不確定也歡迎到現場參觀，會有專人為您介紹」
            """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini 判斷錯誤：", e)
        return "目前服務忙碌中，請稍後再試 🙏"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    print("收到 webhook:", body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print("⚠️ Webhook 錯誤：", e)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_msg = event.message.text.strip()
        reply = get_semantic_faq_or_reply(user_msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except Exception as e:
        print("⚠️ 回覆錯誤：", e)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="發生錯誤了，我們會儘快修復，請稍後再試 🙇")
        )

if __name__ == "__main__":
    app.run(port=5000)
