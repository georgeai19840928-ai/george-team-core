import os
import json
import urllib.request
from datetime import date

TOKEN = os.environ.get("NOTION_TOKEN")
PROJECT_HUB_DS_ID = "bd31c700-142c-476a-bd14-99e36674de90"
GTD_TASKS_DS_ID = "032993e8-3059-433b-b6d5-c0a962c40184"

def notion_request(endpoint, method="POST", data=None):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data: req.data = json.dumps(data).encode("utf-8")
    elif method == "POST": req.data = json.dumps({}).encode("utf-8")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

# 1. Create a specific Project for Deep Research
print("Creating project entry for Deep Research...")
project = notion_request("pages", "POST", {
    "parent": {"type": "data_source_id", "data_source_id": PROJECT_HUB_DS_ID},
    "icon": {"emoji": "🕵️"},
    "properties": {
        "📂 專案名稱": {"title": [{"text": {"content": "[ENGINE-01] DEEP_RESEARCH_MODE"}}]},
        "📡 運行狀態": {"select": {"name": "ACTIVE"}}
    }
})
project_id = project["id"]

# 2. Tasks Decomposed by 0x_Architect
tasks = [
    {"title": "1.1 設計研究主題 JSON Schema", "time": 20, "moscow": "Must", "dod": "產出包含關鍵字、深度、排除項的範例檔案", "risk": ""},
    {"title": "1.2 撰寫 Iterative Search 多步搜尋邏輯腳本", "time": 45, "moscow": "Must", "dod": "腳本能根據初次搜尋結果自動生成下一波關鍵字", "risk": "搜尋死迴圈 -> 加入最大層級限制"},
    {"title": "2.1 實作網域黑名單過濾器", "time": 30, "moscow": "Should", "dod": "成功過濾掉搜尋結果中的廣告與社交平台雜訊", "risk": ""},
    {"title": "2.2 開發並行 web_fetch 抓取模組", "time": 45, "moscow": "Must", "dod": "支援同時抓取 5 個 URL 並具備 Timeout 處理機制", "risk": "網頁擋爬 -> 加入 Random User-Agent"},
    {"title": "2.3 實作抓取失敗備援機制", "time": 15, "moscow": "Must", "dod": "失敗時自動跳過並在日誌記錄 URL，不崩潰", "risk": ""},
    {"title": "3.1 撰寫 Markdown 內容清洗與提取器", "time": 40, "moscow": "Must", "dod": "輸出乾淨的 Markdown 文字，不含 JS/HTML", "risk": ""},
    {"title": "3.2 設計分段摘要 (Chunking) Prompt 協議", "time": 30, "moscow": "Must", "dod": "將長文切分處理後彙整，保留原始引用連結", "risk": "Token 溢出 -> 設定嚴格段落限制"},
    {"title": "3.3 實作多維度趨勢分析邏輯", "time": 45, "moscow": "Should", "dod": "產出結構化的「優勢、風險、技術棧」對比表", "risk": ""},
    {"title": "4.1 建立賽博風格 Markdown 報告樣板", "time": 30, "moscow": "Must", "dod": "樣板包含 Callout、目錄與進度百分比視覺", "risk": ""},
    {"title": "4.2 實作 Notion API 同步報告至每日精華區", "time": 40, "moscow": "Must", "dod": "報告能完美同步至 DAILY_INTEL_LOGS", "risk": ""},
    {"title": "4.3 實作報告寫入失敗重試機制", "time": 20, "moscow": "Should", "dod": "網路波動導致寫入失敗時，能重試 3 次", "risk": ""}
]

print(f"Importing {len(tasks)} atomic tasks...")
for i, t in enumerate(tasks):
    # The first 3 tasks go straight to "Combat Mode" (In Progress)
    # The rest go to Backlog (Next Action)
    is_combat = i < 3
    
    properties = {
        "⚡ 行動指令": {"title": [{"text": {"content": t["title"]}}]},
        "📊 狀態": {"select": {"name": "Next Action"}},
        "📥 快速捕捉": {"checkbox": False},
        "⚔️ 衝刺狀態": {"status": {"name": "In Progress" if is_combat else "Backlog"}},
        "📌 MoSCoW": {"select": {"name": t["moscow"]}},
        "🔋 能量等級": {"select": {"name": "⚡️高能" if t["time"] >= 40 else "🔋低能"}},
        "⏱️ 預估時間(分鐘)": {"number": t["time"]},
        "✅ DoD": {"rich_text": [{"text": {"content": t["dod"]}}]},
        "☠️ Pre-mortem Risk": {"rich_text": [{"text": {"content": t["risk"]}}]},
        "🔗 所屬專案": {"relation": [{"id": project_id}]}
    }
    
    if is_combat:
        properties["🗓️ 執行日期"] = {"date": {"start": date.today().isoformat()}}
        
    notion_request("pages", "POST", {"parent": {"type": "data_source_id", "data_source_id": GTD_TASKS_DS_ID}, "properties": properties})

print("Deep Research Decomposition & Import Complete.")
