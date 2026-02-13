import os
import json
import urllib.request
import sys

TOKEN = os.environ.get("NOTION_TOKEN")
PAGE_ID = os.environ.get("NOTION_PAGE_ID")

if not TOKEN or not PAGE_ID:
    print("Error: NOTION_TOKEN and NOTION_PAGE_ID environment variables must be set.")
    sys.exit(1)

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
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# 1. Cleanup
print("Full purge initiated...")
blocks = notion_request(f"blocks/{PAGE_ID}/children", "GET")
if blocks and "results" in blocks:
    for block in blocks["results"]:
        notion_request(f"blocks/{block['id']}", "DELETE")
    print(f"Purge complete: {len(blocks['results'])} blocks archived.")

# 2. Deploy Strategic Layer: OKRs
print("Deploying Strategic Layer (OKR Protocols)...")
okr_db = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "icon": {"emoji": "🏁"},
    "title": [{"type": "text", "text": {"content": "🏁 STRATEGIC_OBJECTIVES"}}],
    "properties": {
        "Objective": {"title": {}},
        "Quarter": {"select": {"options": [{"name": "Q1"}, {"name": "Q2"}, {"name": "Q3"}, {"name": "Q4"}]}},
        "Status": {"select": {"options": [{"name": "ACTIVE", "color": "blue"}, {"name": "DONE", "color": "green"}]}}
    }
})
okr_id = okr_db["id"]

kr_db = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "icon": {"emoji": "🎯"},
    "title": [{"type": "text", "text": {"content": "🎯 KEY_RESULTS_TRACKER"}}],
    "properties": {
        "Key Result": {"title": {}},
        "Target": {"number": {}},
        "Current": {"number": {}},
        "Objective": {"relation": {"database_id": okr_id, "type": "single_property", "single_property": {}}}
    }
})

# 3. Deploy Tactical Layer: Project Hub
print("Deploying Tactical Layer (Project Hub)...")
project_db = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "icon": {"emoji": "💾"},
    "title": [{"type": "text", "text": {"content": "💾 SYSTEM_PROJECT_HUB"}}],
    "properties": {
        "Project": {"title": {}},
        "Status": {"select": {"options": [{"name": "ACTIVE", "color": "blue"}, {"name": "TESTING", "color": "purple"}]}},
        "Objective": {"relation": {"database_id": okr_id, "type": "single_property", "single_property": {}}}
    }
})
project_id = project_db["id"]

# 4. Deploy Operational Layer: GTD Task Protocol
print("Deploying Operational Layer (GTD Task Protocol)...")
task_db = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "icon": {"emoji": "⚡"},
    "title": [{"type": "text", "text": {"content": "⚡ OPERATION_GTD_TASK"}}],
    "properties": {
        "Task": {"title": {}},
        "Inbox": {"checkbox": {}},
        "Status": {"select": {"options": [{"name": "Inbox", "color": "gray"}, {"name": "Next", "color": "blue"}, {"name": "Waiting", "color": "orange"}, {"name": "Done", "color": "green"}]}},
        "Priority": {"select": {"options": [{"name": "P1-Critical", "color": "red"}, {"name": "P2-High", "color": "orange"}, {"name": "P3-Normal", "color": "blue"}]}},
        "Project": {"relation": {"database_id": project_id, "type": "dual_property", "dual_property": {"synced_property_name": "Tasks"}}}
    }
})

# 5. Dashboard Layout
print("Finalizing Dashboard Layout...")
notion_request(f"blocks/{PAGE_ID}/children", "PATCH", {
    "children": [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "CYBER_BRAIN v3.0 // STRATEGIC COMMAND // MODE: OPTIMIZED", "link": None}, "annotations": {"bold": True, "code": True}}],
                "icon": {"emoji": "🧠"},
                "color": "gray_background"
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "⚡ OPERATIONAL_RADAR (GTD)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Use 'Inbox' view to capture raw thoughts, 'Next' for today's mission."}}]}
        }
    ]
})

print("V3 Deployment Complete.")
