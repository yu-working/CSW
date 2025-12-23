@echo off
:: 1. 切換到當前 .bat 檔案所在的目錄
cd /d %~dp0

:: 2. 檢查是否存在 venv 資料夾 (假設你的虛擬環境資料夾叫 venv)
if not exist ".venv\Scripts\activate" (
    echo [error] cannot find virtual environment. Please set up the virtual environment first.
    pause
    exit
)

echo [system] start venv...
:: 3. 啟動虛擬環境
call .venv\Scripts\activate

echo [system] setting environment variables...
:: 設定環境變數
set DATA_FOLDER=data
set DEFAULT_DATA_FILE=default_data/FAQ_Default.xlsx

echo [system] start Streamlit app...
:: 4. 執行 Streamlit
streamlit run app.py

:: 如果程式被關閉，保持視窗開啟以查看錯誤訊息
pause


:: --- 建議修改這部分以相容 Windows ---
:: DATA_FOLDER = "/app/data"  <-- 這是 Linux 路徑
::DATA_FOLDER = "data"        # 改成這樣，Windows/Linux 都通

:: DEFAULT_DATA_FILE = "/app/default_data/FAQ_Default.xlsx"
::DEFAULT_DATA_FILE = "default_data/FAQ_Default.xlsx"