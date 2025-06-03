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

# Gemini 處理 FAQ 或生成回答
def get_semantic_faq_or_reply(user_input):
    try:
        faq_text_block = "\n".join([
            f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}" 
            for i, item in enumerate(faq_data)
        ])
        prompt = f"""
            你是「毛起來找家」的專業客服人員，請依照以下 FAQ 決定是否能直接回答使用者問題。

            若找到最接近的 FAQ 問題，就直接回覆該問題的對應答案（A#），不需要說明來自 FAQ。
            若 FAQ 無法涵蓋，請依據下列限制條件，自行以繁體中文生成一段簡潔、溫暖且具體的回答。

            FAQ：
            {faq_text_block}

            使用者問題如下：
            「{user_input}」

            回答限制：
            - 僅限於「領養寵物」、「飼養與照顧」、「常見疾病」、「疫苗與防疫」、「飼主責任」、「寵物用品建議」相關主題
            - 若提及想領養某種寵物，請提醒前往「毛起來找家」官網查詢可領養品種
            - 若提及用品，可推薦商品，並加上「若不確定也歡迎到現場參觀，會有專人為您介紹」
            - 回覆時只回答與問題最相關的一段內容，不需一次說明全部資訊
            """
        response = model_gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini 回覆錯誤：", e)
        return "目前服務忙碌中，請稍後再試 🙏"

# === 測試用 CLI ===
if __name__ == "__main__":
    print("🔸 請輸入問題（輸入 q 離開）：")
    while True:
        user_input = input("🧡 請輸入問題：").strip()
        if user_input.lower() == "q":
            break

        print("💬 回覆內容：")
        print(get_semantic_faq_or_reply(user_input))
        print()