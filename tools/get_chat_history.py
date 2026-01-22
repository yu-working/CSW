from mcp.server.fastmcp import FastMCP  # noqa: E402
import os
import re
import json
from typing import Any, Dict, List

mcp = FastMCP("get_chat_history_tool")

def _get_chat_logs_dir() -> str:
    """Return absolute path to data/chat_logs directory from project root."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, "data", "chat_logs")

def _safe_load_json(path: str) -> Dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

@mcp.tool()
def search_chat_history(keyword: str, case_sensitive: bool = False, max_results: int = 50) -> List[Dict[str, Any]]:
    """
    讀取 data/chat_logs/ 下所有 JSON 對話檔，根據「關鍵字」查找相關的聊天記錄。

    參數:
    - keyword: 查找的關鍵字（將在 messages.content、history_list.q、history_list.a 中搜尋）
    - case_sensitive: 是否區分大小寫（預設 False）
    - max_results: 每個檔案最多返回的匹配筆數（預設 50）

    回傳:
    - 由多個檔案組成的列表；每一項包含：
      {
        "file": 檔名,
        "path": 完整路徑,
        "started_at": 對話開始時間（如有）, 
        "timestamp": 最後儲存時間（如有）, 
        "matches": [
           {"type": "message", "index": i, "role": role, "content": content_snippet},
           {"type": "history", "index": i, "q": q_snippet, "a": a_snippet}
        ]
      }
    """

    base_dir = _get_chat_logs_dir()
    if not os.path.exists(base_dir):
        return []

    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        rx = re.compile(re.escape(keyword), flags)
    except Exception:
        # 如果關鍵字不合法，退回到直接字串包含
        rx = None

    results: List[Dict[str, Any]] = []
    files = [fn for fn in os.listdir(base_dir) if fn.lower().endswith(".json")]
    for fn in sorted(files):
        path = os.path.join(base_dir, fn)
        data = _safe_load_json(path)
        if not isinstance(data, dict):
            continue

        messages = data.get("messages") or []
        history_list = data.get("history_list") or []
        started_at = data.get("started_at")
        timestamp = data.get("timestamp")

        matches: List[Dict[str, Any]] = []
        # 搜尋 messages
        for i, m in enumerate(messages):
            try:
                content = (m or {}).get("content") or ""
                role = (m or {}).get("role") or ""
                ok = (rx.search(content) is not None) if rx else (keyword in content if case_sensitive else keyword.lower() in content.lower())
                if ok:
                    snippet = content if len(content) <= 400 else content[:400] + "..."
                    matches.append({"type": "message", "index": i, "role": role, "content": snippet})
                    if len(matches) >= max_results:
                        break
            except Exception:
                continue

        # 若尚未達到上限，再搜尋 history_list
        if len(matches) < max_results:
            for i, h in enumerate(history_list):
                try:
                    q = (h or {}).get("q") or ""
                    a = (h or {}).get("a") or ""
                    ok_q = (rx.search(q) is not None) if rx else (keyword in q if case_sensitive else keyword.lower() in q.lower())
                    ok_a = (rx.search(a) is not None) if rx else (keyword in a if case_sensitive else keyword.lower() in a.lower())
                    if ok_q or ok_a:
                        q_snip = q if len(q) <= 300 else q[:300] + "..."
                        a_snip = a if len(a) <= 300 else a[:300] + "..."
                        matches.append({"type": "history", "index": i, "q": q_snip, "a": a_snip})
                        if len(matches) >= max_results:
                            break
                except Exception:
                    continue

        if matches:
            results.append({
                "file": fn,
                "path": path,
                "started_at": started_at,
                "timestamp": timestamp,
                "matches": matches,
            })

    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")