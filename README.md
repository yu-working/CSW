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

