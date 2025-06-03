## gemini判斷faq或生成回答，加上儲存記憶，第二版
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# === 載入 API 金鑰 ===
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_gemini = genai.GenerativeModel(model_name="gemini-1.5-flash")

# === FAQ 載入 ===
with open("faq2.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)["faq"]

# === 初始化對話歷史 ===
conversation_history = []

# Gemini 處理 FAQ 或生成回答
def get_semantic_faq_or_reply(user_input, history=None, max_history_turns=3):
    try:
        faq_text_block = "\n".join([
            f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}" 
            for i, item in enumerate(faq_data)
        ])

        # 歷史對話內容（最多回顧 n 筆）
        history_block = ""
        if history:
            for turn in history[-max_history_turns:]:
                history_block += f"使用者：{turn['user']}\n客服：{turn['bot']}\n"

        prompt = f"""
            你是「毛起來找家」的專業客服人員，請依照以下 FAQ 判斷是否可以直接回答使用者問題。

            若找到最接近的 FAQ 問題，就直接在結尾括號回覆該問題的對應答案（A#），不需要說明來自 FAQ。
            若 FAQ 無法涵蓋，請根據下方限制條件，自行以繁體中文生成簡潔、溫暖且具體的回覆。
            如果這是持續性的對話，請避免每次回覆都從「您好」開始，改以自然的語氣延續上一輪回應，
            例如「好的，針對您剛剛提到的…」、「如果您考慮退養的話，可以參考以下建議」等方式，使回覆更符合人類對話習慣。


            請注意：
            - 若使用者的語句不完整（如「我想申請」、「需要準備什麼」、「我是第一次養」），請根據上一輪對話主題（例如最近一次提到的寵物種類）進行判斷，延續並補充說明。
            - 若使用者上一輪提到想領養特定動物，請預設當前問題與該動物有關。

            FAQ：
            {faq_text_block}

            先前對話紀錄如下：
            {history_block}

            使用者問題如下：
            「{user_input}」

            回答限制：
            - 若使用者提供基本資料（如姓名、聯絡方式、住址、飼養計畫），系統將回覆「收到您的資料，我們將在三至五個工作天內由專人核實並與您聯繫」
            - 僅限於「領養寵物」、「飼養與照顧」、「常見疾病」、「疫苗與防疫」、「飼主責任」、「寵物用品建議」等主題
            - 若提及想領養某種寵物，請提醒前往「毛起來找家」官網查詢可領養品種。可被領養的動物包含：貓、狗、兔子、天竺鼠、倉鼠，不包括非法或野生動物如熊、老虎等
            - 若提及退養、轉養、寄養等需求，請溫和提醒我們提供臨時退養登記與評估，並將紀錄保留作為未來領養申請的參考依據
            - 若提及拾獲或撿到動物，可提醒我們無法直接收容，但可提供聯絡動保單位、送醫、掃晶片等初步建議
            - 若提及用品，可推薦商品，並補充：「若不確定也歡迎到現場參觀，會有專人為您介紹」
            - 回覆時只針對問題中最重要的主題回答一段內容，避免一次說完所有事情
            """
        response = model_gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini 回覆錯誤：", e)
        return "目前服務忙碌中，請稍後再試 🙏"

# === 測試 CLI ===
if __name__ == "__main__":
    print("🔸 請輸入問題（輸入 q 離開）：")
    while True:
        user_input = input("🧡 請輸入問題：").strip()
        if user_input.lower() == "q":
            break

        reply = get_semantic_faq_or_reply(user_input, history=conversation_history)
        print("💬 回覆內容：")
        print(reply + "\n")

        # 儲存對話歷史
        conversation_history.append({
            "user": user_input,
            "bot": reply
        })