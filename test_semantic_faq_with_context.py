
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

# === 對話歷史紀錄 ===
dialog_history = []

# Gemini 處理 FAQ 或生成回答
def get_semantic_faq_or_reply(user_input):
    try:
        # 建構 FAQ 區塊
        faq_text_block = "\n".join([
            f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}" 
            for i, item in enumerate(faq_data)
        ])

        # 整理對話歷史（最多保留3輪）
        history_text = "\n".join([f"使用者：{q}\n客服：{a}" for q, a in dialog_history[-3:]])

        prompt = f"""
            你是「毛起來找家」的專業客服人員，請依照 FAQ 決定是否能直接回答使用者問題。
            如果找到最接近的 FAQ 問題，就直接回覆該問題的答案（A#），不需說明來自 FAQ。
            若 FAQ 無法涵蓋，請根據下列限制條件，自行以繁體中文生成一段簡潔、溫暖且具體的回答。

            請注意：若使用者的語句不完整（如「我想申請」、「需要準備什麼」），請根據上一輪對話主題進行判斷，延續對話內容進行回應。

            [常見問題 FAQ]
            {faq_text_block}

            [對話歷史]
            {history_text}

            [使用者提問]
            {user_input}

            回答限制：
            - 僅限於「領養寵物」、「飼養與照顧」、「常見疾病」、「疫苗與防疫」、「飼主責任」、「寵物用品建議」相關主題
            - 若提及想領養的動物，請提醒前往「毛起來找家」官網查詢可領養品種（僅限貓、狗、兔子、天竺鼠、倉鼠）
            - 若提及用品，可推薦商品，並加上「若不確定也歡迎到現場參觀，會有專人為您介紹」
            - 回覆時只回答與問題最相關的一段內容，不需一次說明全部資訊
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

        reply = get_semantic_faq_or_reply(user_input)
        dialog_history.append((user_input, reply))

        print("💬 回覆內容：")
        print(reply)
        print()
