import os
import json
import urllib.request

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
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error {method} {endpoint}: {e}")
        return None

def hydrate_project(project_id, project_name):
    print(f"Hydrating project: {project_name} ({project_id})")
    
    # 1. Fetch related tasks
    query = notion_request(f"data_sources/{GTD_TASKS_DS_ID}/query", "POST", {
        "filter": {
            "property": "🔗 所屬專案",
            "relation": {"contains": project_id}
        }
    })
    
    tasks = []
    if query and "results" in query:
        tasks = query["results"]
    
    # 2. Prepare blocks to append
    # We clear old info by finding the blocks we added earlier? 
    # Or just append a fresh list.
    
    children = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🛰️ 任務分流雷達 (Task Satellite)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "此專案目前收容以下原子任務："}}]}
        }
    ]
    
    for task in tasks:
        task_id = task["id"]
        task_title = task["properties"]["⚡ 行動指令"]["title"][0]["text"]["content"]
        # Use a "link_to_page" block or a bullet with a mention
        children.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text", 
                        "text": {"content": "⚡ "},
                        "annotations": {"bold": True}
                    },
                    {
                        "type": "mention",
                        "mention": {
                            "type": "page",
                            "page": {"id": task_id}
                        }
                    }
                ]
            }
        })
    
    # 3. Append to page
    notion_request(f"blocks/{project_id}/children", "PATCH", {"children": children})

# Main execution
projects = [
    {"id": "30652d88-a5a9-8122-8d1f-f888f2955aed", "name": "🦐 數位員工核心功能開發"},
    {"id": "30652d88-a5a9-8117-bfcf-efdbbd494b34", "name": "[ENGINE-01] DEEP_RESEARCH_MODE"}
]

for p in projects:
    hydrate_project(p["id"], p["name"])

print("Project Hydration Complete.")
