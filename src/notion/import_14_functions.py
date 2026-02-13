import os
import json
import urllib.request
import sys

TOKEN = os.environ.get("NOTION_TOKEN")
# Using the data_source IDs found in search
PROJECT_HUB_ID = "bd31c700-142c-476a-bd14-99e36674de90"
GTD_TASKS_ID = "032993e8-3059-433b-b6d5-c0a962c40184"

def notion_request(endpoint, method="POST", data=None):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

# 1. Create the Project
print("Creating project entry...")
project = notion_request("pages", "POST", {
    "parent": {"type": "data_source_id", "data_source_id": PROJECT_HUB_ID},
    "icon": {"emoji": "🦐"},
    "properties": {
        "📂 專案名稱": {"title": [{"text": {"content": "🦐 數位員工核心功能開發"}}]},
        "📡 運行狀態": {"select": {"name": "ACTIVE"}}
    }
})
project_page_id = project["id"]

# 2. Add the 14 Functions as Tasks
functions = [
    "1. 晨間簡報：抓取天氣/日曆/TODO，每日 08:00 推播摘要。",
    "2. GitHub 趨勢：定時搜尋 AI 專案並摘要推播。",
    "3. 社群哨兵：心跳監測 X/Threads 關鍵字，過濾廢話。",
    "4. 郵件秘書：讀取 Gmail 並分類摘要，產出回覆草稿。",
    "5. 成本守門員：每 4 小時監控 Token 消耗並預警。",
    "6. 記憶維護：夜間提煉對話精華更新 MEMORY.md。",
    "7. 專案看板：檢查 git/檔案狀態，自動更新進度條。",
    "8. 訊息整理：每日彙整特定群組技術精華。",
    "9. 智慧提醒：根據對話意圖動態建立提醒任務。",
    "10. 深夜研究：深度主題搜尋並產出研究文檔。",
    "11. 系統健檢：監控伺服器狀態，異常時報警。",
    "12. 任務委派：主從架構分工執行複雜任務。",
    "13. 行事曆助理：分析行程衝突與距離，預警提示。",
    "14. 晚安回顧：總結今日產出並確認明日計畫。"
]

print(f"Adding {len(functions)} tasks...")
for func in functions:
    notion_request("pages", "POST", {
        "parent": {"type": "data_source_id", "data_source_id": GTD_TASKS_ID},
        "properties": {
            "⚡ 行動指令": {"title": [{"text": {"content": func}}]},
            "📊 狀態": {"select": {"name": "Next Action"}},
            "🚨 優先等級": {"select": {"name": "P2-High"}},
            "🔗 所屬專案": {"relation": [{"id": project_page_id}]}
        }
    })

print("Success.")
