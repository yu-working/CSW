import streamlit as st
import pandas as pd
import akasha
import dotenv
import os
import sys

# --- 1. 環境設定 ---
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, ".env")
dotenv.load_dotenv(dotenv_path)

MODEL = os.getenv("MODEL")
data_dir = os.getenv("DATA_DIR", "data.xlsx")

# 假設圖片路徑
# USER_AVATAR = "static/user_icon.png"
# BOT_AVATAR = "https://your-domain.com/bot-logo.png"
# 用法
# with st.chat_message("user", avatar=USER_AVATAR):

# --- 2. 資料讀取 (快取優化) ---
@st.cache_data
def read_excel_sheets():
    # 讀取 Excel 資料
    dfs = pd.read_excel(data_dir, sheet_name=["E管家", "智慧插座", "安裝前中後問題"])
    return dfs

data = read_excel_sheets()

def format_data_for_ai(data_dict):
    full_text = ""
    for name, df in data_dict.items():
        full_text += f"\n--- {name} 知識庫 ---\n"
        full_text += df.to_csv(index=False) # CSV 格式通常對 AI 來說比 to_string 更省 token 且結構清晰
    return full_text

context_data = format_data_for_ai(data)

system_prompt = f"""
你是一名客服人員的助理機器人，客服人員，請注意以下事項：
1. 請先分析提問，是需要一般的問題還是想要從歷史紀錄找出相關資料，如果是一般的問題正常回答即可，如果是想從歷史紀錄找出相關資料，則查找資料{context_data}中有無類似或相關之資訊。
2. 若資料中有相關資訊，請整理並條列式顯示:歷史提問、歷史回答、裝置世代(如有)、類型、流程階段、關鍵字。如有多個相關資訊，請全部條列出來並區隔開來。
3. 若資料中無相關資訊，請分析客戶提問，並給予類型、流程階段(僅包含APP、安裝前、安裝中、安裝後)、關鍵字。
"""

# --- 3. Streamlit 介面設定 ---
st.set_page_config(page_title="CSAST")
st.title("CSAST")

# 初始化會話狀態 (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history_text" not in st.session_state:
    st.session_state.history_text = ""

# 側邊欄：功能按鈕
with st.sidebar:
    # 在側邊欄最上方加入輸入框
    # type="password" 可以隱藏輸入的內容
    user_api_key = st.text_input(
        "輸入您的 API KEY", 
        value=os.getenv("OPENAI_API_KEY", ""), # 預設嘗試讀取 .env
        type="password",
        help="輸入後將優先使用此 Key 進行對話"
    )
    
    # 動態更新環境變數，讓 akasha 能讀取到
    if user_api_key:
        os.environ["GEMINI_API_KEY"] = user_api_key
        st.success("API Key 已就緒！")
    else:
        st.warning("請輸入 API Key 以開始對話")

    st.divider() # 分隔線
    
    if st.button("清除對話歷史"):
        st.session_state.messages = []
        st.session_state.history_text = ""
        st.rerun()

# 顯示現有的對話紀錄
for message in st.session_state.messages:
    avatar_icon = "🦥" if message["role"] == "user" else "🐑"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- 4. 對話邏輯 ---
if prompt := st.chat_input("請問我有什麼可以協助的嗎?"):
    # 顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🦥"):
        st.markdown(prompt)

    # 呼叫 Akasha 模型
    with st.chat_message("assistant", avatar="🐑"):
        with st.spinner("思考中..."):
            ak = akasha.ask(
                model=MODEL,
                temperature=0.1,
                max_input_tokens=20000,
                max_output_tokens=20000
            )
            
            final_prompt = (
                system_prompt + 
                f"\n# 提問: {prompt}" + 
                f"\n# 對話歷史: {st.session_state.history_text}"
            )
            
            response = ak(prompt=final_prompt)
            st.markdown(response)

    # 儲存回覆到紀錄中
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.history_text += f"\n客戶提問: {prompt}\n回覆: {response}"