### 生成式 AI 課程的期末作業

# 🐾 毛起來找家 LINE 智能客服系統

這是一個專為「毛起來找家」設計的智慧型客服系統，整合 LINE Bot、FAQ 語意搜尋與 Gemini 回答備援功能。

## 🚀 功能亮點

- ✅ 語意 FAQ 查詢（使用 SentenceTransformer）
- ✅ Gemini 回覆：當 FAQ 不足時由 Gemini 補充回答
- ✅ 支援 LINE webhook 串接與 Flask server
- ✅ FAQ 可擴充，支援多句式相似語句匹配
- ✅ 可本地測試 FAQ 模組（不需上網）

---

## 📦 安裝方式

### 1. 安裝套件

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install flask line-bot-sdk sentence-transformers python-dotenv google-generativeai
```

---

### 2. 建立 `.env`

請複製 `.env.example` 並建立你的 `.env`：

```bash
cp .env.example .env
```

內容範例如下：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_token
LINE_CHANNEL_SECRET=your_line_secret
GEMINI_API_KEY=your_gemini_api_key
```

---

### 3. 執行方式

#### ✅ FAQ 測試（無需 LINE / Gemini）

```bash
python test_faq_only.py
```

#### ✅ 啟動 Flask + LINE Bot + Gemini

```bash
python app.py
```

可用 [ngrok](https://ngrok.com) 曝露本機 webhook：

```bash
ngrok http 5000
```

---

## 🗂️ 檔案說明

| 檔案名稱           | 說明 |
|--------------------|------|
| `app.py`           | 主系統入口，整合 FAQ + Gemini + LINE webhook |
| `gemini_api.py`    | Gemini 回答模組 |
| `test_faq_only.py` | 本地 FAQ 測試腳本，不需啟動伺服器 |
| `faq.json`         | FAQ 問答集，可擴充多句同義語句 |
| `.env.example`     | 環境變數設定模板 |
| `requirements.txt` | 所需套件列表 |

---

## 🧠 FAQ 模型說明

語意搜尋採用 `sentence-transformers` 的：

**paraphrase-multilingual-MiniLM-L12-v2**  
支援繁體中文語意比對與模糊查詢。

---

## 🔗 參考來源

- OXXO Studio LINE 教學：[LINE Bot 基礎教學](https://steam.oxxostudio.tw/category/python/example/line-developer.html)
- [如何使用 ngrok 建立本地 webhook](https://steam.oxxostudio.tw/category/python/example/ngrok.html#a2)
- [LINE Webhook 實作](https://steam.oxxostudio.tw/category/python/example/line-webhook.html)
- 感謝 [OpenAI ChatGPT](https://openai.com/chatgpt) 協助整合與說明

---

## 📄 授權

本專案開源，歡迎學習與修改，可依據 [MIT License] 或依實際需求指定。
