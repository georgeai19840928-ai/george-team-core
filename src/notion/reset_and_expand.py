import os
import json
import urllib.request

TOKEN = os.environ.get("NOTION_TOKEN")
PAGE_ID = os.environ.get("NOTION_PAGE_ID")
# Using the data_source ID for GTD_TASKS
GTD_TASKS_DS_ID = "032993e8-3059-433b-b6d5-c0a962c40184"

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
    elif method == "POST":
        req.data = json.dumps({}).encode("utf-8")
        
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
        return None

# 1. Reset Tasks to Inbox
print("Scanning for tasks to reset...")
query_results = notion_request(f"data_sources/{GTD_TASKS_DS_ID}/query", "POST")
if query_results and "results" in query_results:
    for page in query_results["results"]:
        page_id = page["id"]
        print(f"Resetting task: {page_id}")
        notion_request(f"pages/{page_id}", "PATCH", {
            "properties": {
                "📊 狀態": {"select": {"name": "Inbox"}},
                "📥 快速捕捉": {"checkbox": True}
            }
        })

# 2. Create Daily Intel Logs Database
print("Creating Daily Intel Logs Database...")
intel_logs_db = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "icon": {"emoji": "📖"},
    "title": [{"type": "text", "text": {"content": "📅 每日對話精華 (DAILY_INTEL_LOGS)"}}],
    "properties": {
        "日期檔案": {"title": {}},
        "紀錄日期": {"date": {}},
        "精華標籤": {"multi_select": {"options": [
            {"name": "技術決策", "color": "blue"},
            {"name": "功能拆解", "color": "purple"},
            {"name": "系統修復", "color": "red"}
        ]}},
        "對話連結": {"url": {}}
    }
})

if intel_logs_db:
    db_id = intel_logs_db["id"]
    print(f"Successfully created Intel Logs DB: {db_id}")
    
    # 3. Update Dashboard Layout
    notion_request(f"blocks/{PAGE_ID}/children", "PATCH", {
        "children": [
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📜 HISTORICAL_INTEL_LOGS"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "This database stores nightly distillations of conversations."}}]
                }
            }
        ]
    })

print("Process Complete.")
