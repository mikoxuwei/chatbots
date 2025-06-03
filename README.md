# 🐾 毛起來找家 LINE 智能客服系統

這是一個專為「毛起來找家」設計的智慧型客服系統，整合 LINE Bot、語意 FAQ 查詢與 Gemini AI 回答備援功能，並支援多輪對話記憶與自然語氣回應。

---

## 🚀 功能亮點

- ✅ Gemini AI 語意理解與生成回應（Google Generative AI）
- ✅ 整合 FAQ 問答集，由 Gemini 自動判斷是否套用現有答案（並註記 A# 編號）
- ✅ 對話記憶功能：根據上下文理解語意、延續回應主題
- ✅ 回應語氣自然化，避免每次重複打招呼，更貼近人類客服
- ✅ 提供 LINE webhook 串接 + Flask 應用整合
- ✅ 支援本地測試 FAQ 模組

---

## 📦 安裝方式

### 1. 安裝套件

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install flask line-bot-sdk python-dotenv google-generativeai
```

---

### 2. 建立 `.env` 檔

```bash
cp .env.example .env
```

填入以下內容：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_token
LINE_CHANNEL_SECRET=your_line_secret
GEMINI_API_KEY=your_gemini_api_key
```

---

### 3. 執行方式

#### ✅ 啟動主系統（整合 Gemini + LINE Bot + FAQ）

```bash
python final_linebot.py
```

#### ✅ 使用 ngrok 曝露 webhook

```bash
ngrok http 5000
```

#### ✅ Gemini 本地測試（整合 FAQ 語意比對 + Gemini 回覆）

```bash
python test_faq_memory2.py
```

- 可支援上下文記憶對話。
- 使用者輸入若與 FAQ 相符，回覆 FAQ 答案（包含編號），否則請 Gemini 產生新回應。
- 模擬實際客服對話，不需連接 LINE Bot。

---

## 🧠 FAQ 機制說明

FAQ 資料儲存在 `faq.json` 中，包含多筆常見問答。主系統透過 Gemini 語意模型自動比對並選擇最適合的回應。

- 若命中 FAQ，系統將使用該答案，並附註編號（如 A4）
- 若無 FAQ 覆蓋，則由 Gemini 生成回應
- 支援 FAQ 主題包括：領養申請、條件、用品推薦、退養、動物救援流程等

---

## 🗂️ 檔案說明

| 檔案名稱           | 說明 |
|--------------------|------|
| `final_linebot.py` | 主系統入口，整合 LINE webhook + FAQ 判斷 + Gemini 回覆 |
| `test_faq_memory2.py` | 本地測試 FAQ + Gemini 回覆（支援上下文記憶） |
| `faq.json`         | 常見問答集，會被 Gemini 引用於比對與回覆 |
| `gemini_api.py`    | Gemini 語意產生器備用模組 |
| `.env.example`     | 環境變數模板 |
| `requirements.txt` | 套件需求列表 |

---

## 🔗 參考來源

- OXXO Studio LINE 教學：[LINE Bot 基礎教學](https://steam.oxxostudio.tw/category/python/example/line-developer.html)
- [ngrok 建立 webhook 教學](https://steam.oxxostudio.tw/category/python/example/ngrok.html#a2)
- [LINE webhook 實作](https://steam.oxxostudio.tw/category/python/example/line-webhook.html)
- 感謝 [OpenAI ChatGPT](https://openai.com/chatgpt) 協助整合與說明

---

## 📄 授權 License

本專案以 MIT 授權開源，歡迎自由學習、應用與修改。