import pandas as pd
import akasha  # noqa: E402
import dotenv
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, ".env")
dotenv.load_dotenv(dotenv_path)

MODEL = os.getenv("MODEL")
data_dir = os.getenv("DATA_DIR", "data.xlsx")
def read_excel_sheets():
    dfs = pd.read_excel(data_dir, sheet_name=["E管家", "智慧插座", "安裝前中後問題"])

    return dfs

data = read_excel_sheets()

system_prompt = f"""
        你是一名客服人員的助理機器人，請根據輸入的客戶提問，協助客服人員查找相關資料{data}，請注意以下事項：
        1. 請先分析客戶提問，查找資料中有無類似或相關之資訊。
        2. 若資料中有相關資訊，請整理並條列式顯示:歷史提問、歷史回答、裝置世代(如有)、類型、流程階段、關鍵字。
        3. 若資料中無相關資訊，請分析客戶提問，並給予類型、流程階段(僅包含APP、安裝前、安裝中、安裝後)、關鍵字。
        """

ak = akasha.ask(
    model=MODEL,
    temperature=0.1,
    max_input_tokens=20000,
    max_output_tokens=20000
)
history = ""
while True:
    question = input("請問我有什麼可以協助的嗎: ")
    
    if question.lower() in ["exit", "quit","e","q"]:
        break
    if question.lower() in ["clear"]:
        history = ""
        print("對話歷史已清除。")
        continue
    final_prompt = system_prompt + f"\n# 客戶提問: {question}" + f"\n# 對話歷史: {history}"
    res = ak(
        prompt=final_prompt,
    )
    print("Final response:")
    print(res)
    history = history + f"\n客戶提問: {question}\n回覆: {res}"

