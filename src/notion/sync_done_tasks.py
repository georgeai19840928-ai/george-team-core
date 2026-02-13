import os
import json
import urllib.request

TOKEN = os.environ.get("NOTION_TOKEN")

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

task_ids = [
    "30652d88-a5a9-819c-a8d8-e4e4448085c0", # 1.1
    "30652d88-a5a9-8140-94d3-f2a25afc7b11", # 1.2
    "30652d88-a5a9-8185-bc46-c951cc883465"  # 2.1
]

print("Updating Notion tasks to DONE...")
for tid in task_ids:
    notion_request(f"pages/{tid}", "PATCH", {
        "properties": {
            "📊 狀態": {"select": {"name": "Done"}},
            "⚔️ 衝刺狀態": {"status": {"name": "Done"}}
        }
    })
print("Notion Sync Complete.")
