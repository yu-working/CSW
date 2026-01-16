# Customer Service Wingman

> 客服助手系統終端

這個程式是一個專門為 客服人員 設計的智慧工具，目的是讓您在回答客戶問題時，能夠更快、更準確地找到標準答案和相關資訊。

您只需要:
1. 輸入客戶問題
    - 程式會幫您檢索所有關於「E管家」、「智慧插座」以及各種「安裝前中後問題」的歷史客服記錄，並找出相關的提問資料。
2. 獲取結構化回覆
    - 程式會在幾秒鐘內，給您一份條列式、整理好重點的參考資訊
---

## 功能

* **關鍵功能 1**: 根據客戶的提問，檢索歷史紀錄中相關的提問並進行回應
* **關鍵功能 2**: 通過語言模型自動產生回應建議，並提供參考資料

---

## 對話組與記錄

- **對話組**: 每一組對話都儲存在同一個檔案中（位於 `data/chat_logs/`，檔名格式為 `YYYYMMDD_HHMMSS.json`）。
- **目前對話檔案**: 由 [data_state.json](data_state.json) 的 `chat_state.active_file` 追蹤，重新整理頁面後仍會指向同一檔案。
- **建立新對話**: 在側邊欄的「對話組」點選「開啟新對話」，會建立新檔並切換到該檔案。
- **載入舊對話**: 在側邊欄選擇既有檔案後按「載入舊對話」，會切換目前對話檔案並載入其內容顯示。
- **自動儲存**: 每次助理回覆後，自動覆寫目前對話檔案中的 `messages` 與 `history_list`，不會額外新增新檔案。

---

## 專案架構

```
CSW/
├── app.py               # 主程式
├── cli.py               # cli服務
├── start.bat            # 資料庫插入操作
├── requirements.txt     # Python 相依套件
├── Dockerfile           # Docker 設定檔
├── .env                 # 環境變數設定
└── default_data/
    └── FAQ_Default.xlsx # 預設問答紀錄文件
```

---

## 快速開始

### **本地網頁**

1.  **複製儲存庫 (Clone the repo)**
    ```bash
    git clone https://github.com/yu-working/CSW.git
    cd CSW
    ```

2.  **通過uv建立虛擬環境並安裝套件**

3.  **新增預設檔案**
    在 `default_data/FAQ_Default.xlsx` 

3.  **雙擊 `start.bat` 啟動應用**

---

### **SERVER服務**

1.  **複製儲存庫 (Clone the repo)**
    ```bash
    git clone https://github.com/yu-working/CSW.git
    cd CSW
    ```

2.  **啟動DOCKER並建立image**
    ```bash
    docker build -t csw .
    ```

3.  **啟動容器**
    ```
    docker run ^
    -v C:\path\to\data:/app/data ^
    -d -p 8501:8501 ^
    --name csw csw
    ```

4.  **使用服務**
    開啟 `localhost:8501` 檢視服務是否成功啟動

