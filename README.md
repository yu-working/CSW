# CSAST

> 客服助手系統終端

專案的詳細描述，說明它的用途、解決了什麼問題，以及它的主要功能。

---

## ✨ 功能

* **關鍵功能 1**: 根據客戶的提問，檢索歷史紀錄中相關的提問並進行回應
* **關鍵功能 2**: 通過語言模型自動產生回應建議，並提供參考資料(開發中...)

---

## 快速開始

### 前提

已安裝conda==4.10.3

### 安裝

1.  **複製儲存庫 (Clone the repo)**
    ```bash
    git clone https://github.com/yu-working/CSAST.git
    cd CSAST
    ```

2.  **安裝依賴項 (Install dependencies)**
    ```bash
    pip install -r requirements.txt
    ```

3.  **新增環境變數在根目錄**
    ```
    GEMINI_API_KEY={your_api_key}
    MODEL={your_model_name} #e.g. gemini:gemini-2.5-flash
    DATA_DIR={your_data_xlsx} #default:"data.xlsx"
    ```

4.  **啟動專案 (Run the project)**
    ```bash
    python main.py
    ```

---

## 🛠 使用方法
成功啟動程式後，可以看到:
```bash
請問我有什麼可以協助的嗎: 
```

### 直接輸入客戶的提問:
```bash
請問我有什麼可以協助的嗎: 要怎麼開通
```
語言模型會檢索最相似的歷史紀錄並進行回應

Final response:
根據您提供的客戶提問「要怎麼開通」，我在參考資料中找到以下相關資訊：
```
*   **歷史提問:** 如何開通？
*   **歷史回答:** 先生您好，要麻煩您先填安裝同意書，繳交給物業，等到裝置安裝上後，之後才會進行開通服務。謝謝
*   **裝置世代:** RouteB
*   **型別:** 開通
*   **流程階段:** E管家平臺/APP
*   **關鍵字:** 開通, 安裝同意書, 物業, 裝置安裝
```

### 退出
```bash
請問我有什麼可以協助的嗎: exit
#或
請問我有什麼可以協助的嗎: quit
請問我有什麼可以協助的嗎: e
請問我有什麼可以協助的嗎: q
```
即可結束程式