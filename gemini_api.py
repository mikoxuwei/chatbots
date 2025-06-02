import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 改用 flash 模型以避免 429
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_gemini_reply(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        print("Gemini 錯誤：", e)
        return "目前服務忙碌中，請稍後再試 🙏"
