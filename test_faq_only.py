import json
import jieba
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 讀取 FAQ
with open("faq2.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)["faq"]

faq_questions = [item["question"] for item in faq_data]
faq_answers = [item["answer"] for item in faq_data]

# 初始化語意模型
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
faq_embeddings = model.encode(faq_questions)

def search_faq_semantic(user_input, threshold=0.6):
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, faq_embeddings)[0]
    best_idx = similarities.argmax()
    if similarities[best_idx] >= threshold:
        return faq_answers[best_idx]
    return "（找不到符合的 FAQ，請改問其他問題）"

# 測試用互動介面
print("🐾 歡迎來到『毛起來找家』常見問答系統，請輸入問題（輸入 'exit' 離開）：")
while True:
    query = input("🧡 請輸入問題：").strip()
    if query.lower() == 'exit':
        break
    reply = search_faq_semantic(query)
    print(f"💬 回覆內容：{reply}\n")