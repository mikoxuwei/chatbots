from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os, json, jieba
import google.generativeai as genai

# === 環境設定 ===
load_dotenv()
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# === Gemini 設定 ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# === FAQ 載入與轉向量 ===
with open("faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)["faq"]
faq_questions = [item["question"] for item in faq_data]
faq_answers = [item["answer"] for item in faq_data]

model_embed = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
faq_embeddings = model_embed.encode(faq_questions)

# === 語意 FAQ 搜尋 ===
def search_faq(user_input, threshold=0.6):
    user_vec = model_embed.encode([user_input])
    scores = cosine_similarity(user_vec, faq_embeddings)[0]
    best_idx = scores.argmax()
    if scores[best_idx] >= threshold:
        return faq_answers[best_idx]
    return None

# Gemini 回覆封裝（含 try-except）
def get_gemini_reply(user_input):
    try:
        prompt = f"""
你是「毛起來找家」的一位專業寵物顧問，請以溫暖、清楚、具體的繁體中文回答使用者的問題。

「毛起來找家」是一間專門協助領養貓咪、狗狗、天竺鼠等動物的單位，也有販售少量寵物相關用品。

請依據以下限制回答問題：
- 僅回答與「領養寵物」、「飼養與照顧」、「常見疾病」、「疫苗與防疫」、「飼主責任」、「寵物用品建議」等主題相關的問題
- 回答時若使用者詢問領養某種寵物，請提醒可至「毛起來找家」的官網查詢目前可領養的品種
- 若使用者詢問用品，也可適度推薦商品，但結尾可加上「若不確定也歡迎到現場參觀，會有專人為您介紹」

請根據提問的主題，**只回答與該問題直接相關的一小段內容**，不需要一次講完所有資訊。

若對方問的比較廣泛，也請**先從最關鍵資訊說明起，再詢問是否想進一步了解某方面內容**，例如：環境、飲食或用品。

使用者提問如下：
「{user_input}」
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("⚠️ Gemini 錯誤：", e)
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
        print("⚠️ Webhook 處理錯誤：", e)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_msg = event.message.text.strip()
        
        # 先試著從 FAQ 找答案
        reply = search_faq(user_msg, faq_data)

        # 如果沒有符合的 FAQ，則請 Gemini 幫忙回答
        if not reply:
            reply = get_gemini_reply(user_msg)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except Exception as e:
        print("⚠️ 訊息處理錯誤：", e)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="發生錯誤了，我們會儘快修復，請稍後再試 🙇")
        )

if __name__ == "__main__":
    app.run(port=5000)