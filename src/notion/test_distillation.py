import os
import json
import urllib.request
from datetime import datetime

TOKEN = os.environ.get("NOTION_TOKEN")
INTEL_LOGS_DB_ID = "e5070b2f-a450-4e63-aa56-6fb3799a4c2c"

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

def create_intel_log(date_str, summary_content):
    print(f"Creating intel log for {date_str}...")
    notion_request("pages", "POST", {
        "parent": {"type": "database_id", "database_id": INTEL_LOGS_DB_ID},
        "properties": {
            "日期檔案": {"title": [{"text": {"content": date_str}}]},
            "紀錄日期": {"date": {"start": date_str}},
            "精華標籤": {"multi_select": [{"name": "技術決策"}, {"name": "功能拆解"}]}
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "核心摘要"}}] }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": summary_content}}] }
            }
        ]
    })

# Distillation content
logs = [
    {
        "date": "2026-02-12",
        "summary": "1. 團隊正式成立，擔任 PM 與 DevOps 角色。\n2. 啟動 ai-trend-watcher 專案，成功配置 Zeabur 自動化部署。\n3. 排除 GitHub API 422 錯誤，優化趨勢搜尋邏輯。"
    },
    {
        "date": "2026-02-13",
        "summary": "1. 深度研究 OpenClaw 自動化藍圖，拆解 14 項核心功能工作流。\n2. 部署賽博龐克 Notion 數位大腦 v3.1，整合 OKR/Project/GTD 三層架構。\n3. 完成中文化語言包部署，確立「Inbox -> Triage -> Next Action」工作協議。"
    }
]

for log in logs:
    create_intel_log(log["date"], log["summary"])

print("Nightly distillation test completed.")
