# Customer Service Wingman (CSW)

> 客服助手系統前端（Streamlit）

CSW 是為客服人員打造的智慧助理工具。它能彙整知識庫、呼叫外部工具查詢客戶資訊，並自動生成結構化的回覆建議，協助你更快且精準地回應客戶。

---

## 特色功能

- 回答生成：根據提問與已選知識庫，輸出條列、可複製的建議回覆（以程式碼區塊包裝，已啟用自動換行）。
- 知識庫管理：支援上傳並選擇多個資料檔（xlsx/docx/txt/pdf/pptx），即時生效；也可直接在側邊欄刪除檔案。
- 對話管理：對話檔自動儲存於 `data/chat_logs/`，檔名由語言模型依第一句提問語意生成（顯示時不含 `.json`）。
- 對話操作：可立即載入、重新命名，或刪除對話（刪除按鈕已加強紅色粗體視覺提醒）。
- 模型與 API Key：可在側邊欄切換模型來源，並輸入對應的 API Key 即可開始使用。
- MCP 工具整合：內建 `get_user_info` 工具（Python 腳本）可查詢客戶基本資料並納入回覆。

---

## 專案架構

```
customer_service_wingman/
├─ app.py                    # 主介面（Streamlit）
├─ cli.py                    # 命令列互動範例（非必要）
├─ start.bat                 # Windows 一鍵啟動（啟用 .venv 後執行 Streamlit）
├─ requirements.txt          # 相依套件
├─ Dockerfile                # Docker 建置與執行
├─ data_state.json           # 目前資料/對話狀態（自動維護）
├─ data/
│  └─ chat_logs/             # 對話記錄（已加入 .gitignore）
├─ default_data/
│  ├─ FAQ_Default.xlsx       # 預設知識庫（使用者提供；首次啟動會複製到 data/）
│  ├─ not_routeb_device.csv  # 非 routeb 用戶資料（姓名、社區名稱、行政區、綁定家電）
│  ├─ routeb_base_info.csv   # routeb 基本資訊（姓名、社區）
│  └─ routeb_questionnaire.csv # routeb 問卷（user_name、community、area、question、answer）
├─ static/                   # 頭像等靜態資源
└─ tools/
   └─ get_user_info.py       # MCP 工具（查詢客戶資訊）
```

---

## 安裝與執行

### 本機（Windows）

1. 建立虛擬環境並安裝套件
```powershell
Invoke-Expression (Invoke-RestMethod "https://raw.githubusercontent.com/yu-working/CSW/master/setup.ps1")
```

2. 準備預設資料
- 確認 `default_data/FAQ_Default.xlsx` 存在；啟動時會自動複製到 `data/FAQ_Default.xlsx`。

3. 啟動應用
- 直接雙擊 `start.bat`，或在已啟用虛擬環境後執行：
```bat
streamlit run app.py
```

4. 開啟瀏覽器
- 前往 http://localhost:8501

### 伺服器（Docker）

1. 建置映像
```bash
docker build -t csw .
```

2. 執行容器（Windows PowerShell 範例）
```powershell
docker run `
  -v C:\path\to\data:/app/data `
  -e DEFAULT_DATA_FILE=/app/default_data/FAQ_Default.xlsx `
  -p 8501:8501 -d --name csw csw
```

3. 使用服務
- 瀏覽 http://localhost:8501

---

## 模型與 API Key 設定

在側邊欄「模型與 API 設定」中：
- 先選擇模型來源，再輸入對應的 API Key。
- 目前支援：
  - Google Gemini (2.5-flash)：環境變數 `GEMINI_API_KEY`
  - OpenAI (GPT-4o / GPT-5)：環境變數 `OPENAI_API_KEY`
  - Anthropic Claude：環境變數 `ANTHROPIC_API_KEY`
- 介面會送出一次測試請求驗證 Key 是否有效。

---

## 知識庫與資料管理

 - 預設資料：
   - 系統會使用 `default_data/FAQ_Default.xlsx` 作為預設知識庫（首次啟動複製到 `data/`）。此檔案內容需由使用者提供
   - 客戶資訊查詢用 CSV（位於 `default_data/`，需自行提供）：
     - `not_routeb_device.csv`：姓名、社區名稱、行政區、綁定家電。
     - `routeb_base_info.csv`：姓名、社區。
     - `routeb_questionnaire.csv`：user_name、community、area、question、answer（會從含「您家中是否有下列電器」且 answer 為「有」的題目擷取家電）。
- 上傳資料：在側邊欄「選擇生效檔案與刪除」上傳 `xlsx/docx/txt/pdf/pptx`。
- 勾選生效：勾選要生效的檔案，畫面會自動重載目前知識庫內容。
- 刪除檔案：同一區塊可多選檔案刪除（刪除後將自動更新生效清單）。
- 狀態儲存：`data_state.json` 會同步保存目前模式與生效清單，重新整理後仍生效。

---

## 對話管理（對話組）

- 新對話：按「開啟新對話」只會重置工作區，不會立刻建立檔案。
- 首則訊息後建立檔案：當你送出第一則訊息並收到助理回覆時，系統會以語言模型根據「第一句提問」產生對話檔名，並建立於 `data/chat_logs/`。
- 對話命名：檔名會自動避免標點、特殊符號，顯示時不含 `.json`；若重複會自動加編號。
- 載入對話：在選單選取後即時載入，不需額外按鈕。
- 重新命名：輸入新名稱並確認即可（同名自動避開衝突）。
- 刪除對話：提供紅色粗體刪除按鈕；若刪除的是目前對話，會重置對話狀態。
- 自動儲存：每次助理回覆後會自動更新目前對話的 `messages` 與 `history_list`。

> 版本控制注意：`data/chat_logs/` 已加入 `.gitignore`，對話內容不會被提交到 Git。

---

## 自訂頭像（Avatar）

- 檔案位置：將頭像圖片放在 `static/` 資料夾。
- 預設檔名：
  - 助理頭像：`static/csw_icon.jpg`
  - 使用者頭像：`static/user_icon.jpg`
- 更換方式：以相同檔名覆蓋即可，建議使用正方形 JPG/PNG。

---

## 開發與除錯

- 需求安裝：`pip install -r requirements.txt`
- 本機啟動：`streamlit run app.py`
- 常見錯誤：
  - 缺少 `default_data/FAQ_Default.xlsx`：請放置檔案後重新整理頁面。
  - API Key 驗證失敗：請確認對應模型與 Key 是否正確；代理或防火牆可能影響請求。
  - 8501 連不到：檢查防火牆或是否已有其他服務佔用該埠。
  - 找不到工具腳本：確認 `tools/get_user_info.py` 是否存在。

---

## 授權

本專案採用 [LICENSE](LICENSE) 所述授權條款。

