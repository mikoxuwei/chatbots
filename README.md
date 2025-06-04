# 🐾 毛起來找家 LINE 智能客服系統

本專案是「生成式 AI 課程」期末作業，打造一套以 LINE Bot 為介面，整合 LINE Bot、語意 FAQ 查詢與 Gemini AI 回答備援功能，並支援多輪對話記憶與自然語氣回應的智慧客服系統，模擬實際應用場景：「毛起來找家」動物領養平台。

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
python final_app.py
```

#### ✅ 使用 ngrok 建立公開網址並串接 LINE Webhook
 當你在本地端執行 Flask 應用程式時（預設監聽 `http://localhost:5000`），LINE 是無法直接連線到你電腦的。這時可以使用 ngrok 將你的本地伺服器「公開（Expose）」到網際網路。

步驟 1：執行 ngrok
```bash
ngrok http 5000
```
執行後，會顯示一個網址，像這樣：
```bash
https://abc123.ngrok.io # 這個網址就是你本機的公開入口
```
步驟 2：填入 LINE Developers 的 Webhook URL
    
1. 前往 LINE Developers 官方網站

2. 登入後，進入你的 Messaging API channel

3. 點選左側的「Messaging API」

4. 找到「Webhook URL」欄位，填入：
    ```bash
    https://abc123.ngrok.io/callback
    ```
> [!NOTE]
> /callback 是你的 Flask app 中對應的接收路徑，請確認與程式碼一致。

步驟 3：測試 Bot 是否連接成功

- 在手機上加入你的 LINE 官方帳號，並發送訊息。若一切設定正確，你的本地應用程式應會在終端機中顯示收到的 webhook 內容，且會由 Gemini + FAQ 回覆你訊息 🎉

#### ✅ Gemini 本地測試（整合 FAQ 語意比對 + Gemini 回覆）

```bash
python gemini_test.py
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
| `final_app.py` | 主系統入口，整合 LINE webhook + FAQ 判斷 + Gemini 回覆 |
| `gemini_test.py` | 本地測試 FAQ + Gemini 回覆（支援上下文記憶） |
| `faq.json`         | 常見問答集，會被 Gemini 引用於比對與回覆 |
| `.env.example`     | 環境變數模板 |
| `requirements.txt` | 套件需求列表 |

---

# 更新

## ☁️ Render 部署說明
後來希望讓 LINE Bot 持續運作，而無需每次手動啟動 Flask 應用程式與 ngrok，所以將專案部署至 Render 平台。
Render 提供免費的 Web Service 部署方案，適合開發與測試用途。

## 🔧 部署步驟

#### 1. 將專案上傳至 GitHub

#### 2. 確保您的專案已推送至 GitHub，並且 .env 檔案已加入 .gitignore，避免洩漏敏感資訊。

#### 3. 建立 Render Web Service

#### 4. 登入 Render 並建立新的 Web Service。

#### 5. 連接您的 GitHub 儲存庫。

#### 6. 設定以下參數：
    ```bash
    Build Command: pip install -r requirements.txt
    Start Command: gunicorn final_app:app
    Environment: 選擇 Python 3
    ```

#### 7. 設定環境變數

> 在 Render 的服務設定中，點選左側的「Environment」。

> 新增以下環境變數：

    ```bash
    LINE_CHANNEL_ACCESS_TOKEN: 您的 LINE Channel Access Token

    LINE_CHANNEL_SECRET: 您的 LINE Channel Secret

    GEMINI_API_KEY: 您的 Gemini API 金鑰
    ```

#### 8. 設定 Webhook URL
> 部署完成後，Render 會提供一個公開的網址，例如：
    ```bash
    https://your-app-name.onrender.com
    ```
> 前往 LINE Developers 平台，進入您的 Messaging API 頻道設定頁面。

> 在「Webhook URL」欄位填入：
    ```bash
    https://your-app-name.onrender.com/callback
    ```
---

## 🔗 參考來源

- OXXO Studio LINE 教學：[LINE Bot 基礎教學](https://steam.oxxostudio.tw/category/python/example/line-developer.html)
- [ngrok 建立 webhook 教學](https://steam.oxxostudio.tw/category/python/example/ngrok.html#a2)
- [LINE webhook 實作](https://steam.oxxostudio.tw/category/python/example/line-webhook.html)
- 感謝 [OpenAI ChatGPT](https://openai.com/chatgpt) 協助整合與說明

---

## 📄 授權 License

本專案以 MIT 授權開源，歡迎自由學習、應用與修改。

## 📢 免責聲明 Disclaimer

本專案為生成式 AI 課程之期末作業，所使用之名稱「毛起來找家」為學生自創。
本專案與該網站無任何關聯，亦無意模仿或冒用。僅作為學術與程式開發練習用途，不具商業意圖。
如有不妥之處，敬請來信指正，我們將即時更正。
