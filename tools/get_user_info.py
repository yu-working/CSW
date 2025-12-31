from mcp.server.fastmcp import FastMCP  # noqa: E402
import os
import re
import pandas as pd

mcp = FastMCP("get_user_info_tool")

@mcp.tool()
def get_base_info(username: str):
    """
    讀取 default_data 的三個 CSV，根據使用者姓名回傳基本資訊：
    - 姓名
    - 是否屬於 routeb（姓名存在於 not_routeb_device.csv 則為 False；存在於其他 CSV 則為 True）
    - 社區（優先來自對應資料集）
    - 行政區（優先來自問卷 routeb_questionnaire.csv 的 area；非 routeb 用戶來自 not_routeb_device.csv 的 行政區）
    - 所持有電器（非 routeb 用戶來自 not_routeb_device.csv 的 綁定家電；routeb 用戶從問卷中「您家中是否有下列電器」且答案為「有」提取）
    回傳: dict
    """

    def safe_read_csv(path: str) -> pd.DataFrame | None:
        if not os.path.exists(path):
            return None
        try:
            return pd.read_csv(path, encoding="utf-8")
        except Exception:
            try:
                return pd.read_csv(path)
            except Exception:
                return None

    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "default_data")
    nr_path = os.path.join(base_dir, "not_routeb_device.csv")
    rq_path = os.path.join(base_dir, "routeb_questionnaire.csv")
    rb_path = os.path.join(base_dir, "routeb_base_info.csv")

    df_nr = safe_read_csv(nr_path)
    df_rq = safe_read_csv(rq_path)
    df_rb = safe_read_csv(rb_path)

    result = {
        "姓名": username,
        "屬於routeb(裝置世代)": None,
        "社區": None,
        "行政區": None,
        "所持有電器": [],
    }

    # 非 routeb：依 not_routeb_device.csv 判定與取得資訊
    if isinstance(df_nr, pd.DataFrame) and "姓名" in df_nr.columns:
        df_nr_user = df_nr[df_nr["姓名"].astype(str) == str(username)]
        if not df_nr_user.empty:
            result["屬於routeb(裝置世代)"] = False
            # 社區名稱、行政區
            if "社區名稱" in df_nr_user.columns:
                result["社區"] = df_nr_user.iloc[0]["社區名稱"]
            if "行政區" in df_nr_user.columns:
                result["行政區"] = df_nr_user.iloc[0]["行政區"]
            # 電器清單
            if "綁定家電" in df_nr_user.columns:
                devices = (
                    df_nr_user["綁定家電"].dropna().astype(str).str.strip().tolist()
                )
                # 去重並過濾空字串
                result["所持有電器"] = sorted({d for d in devices if d})
            return result

    # routeb：存在於 base_info 或 questionnaire
    found_routeb = False
    community = None
    area = None
    devices_routeb: list[str] = []

    if isinstance(df_rb, pd.DataFrame) and {"社區", "姓名"}.issubset(df_rb.columns):
        df_rb_user = df_rb[df_rb["姓名"].astype(str) == str(username)]
        if not df_rb_user.empty:
            found_routeb = True
            community = df_rb_user.iloc[0]["社區"]

    if isinstance(df_rq, pd.DataFrame) and {"user_name", "community"}.issubset(df_rq.columns):
        df_rq_user = df_rq[df_rq["user_name"].astype(str) == str(username)]
        if not df_rq_user.empty:
            found_routeb = True
            if community is None:
                community = df_rq_user.iloc[0]["community"]
            if "area" in df_rq_user.columns:
                area = df_rq_user.iloc[0]["area"]
            # 從問卷提取電器（有）
            if {"question", "answer"}.issubset(df_rq_user.columns):
                mask_device_q = df_rq_user["question"].astype(str).str.contains("您家中是否有下列電器", na=False)
                mask_have = df_rq_user["answer"].astype(str) == "有"
                df_devices = df_rq_user[mask_device_q & mask_have]
                for q in df_devices["question"].astype(str).tolist():
                    # 取出中括號內容
                    m = re.search(r"\[(.*?)\]", q)
                    if m:
                        devices_routeb.append(m.group(1))

    if found_routeb:
        result["屬於routeb(裝置世代)"] = True
        result["社區"] = community
        result["行政區"] = area
        result["所持有電器"] = sorted({d for d in devices_routeb if d})
        return result

    # 未找到：保持 None/空集合
    return result

if __name__ == "__main__":
    # a = get_base_info("張家綺")    
    # print(a) 
    mcp.run(transport="stdio")