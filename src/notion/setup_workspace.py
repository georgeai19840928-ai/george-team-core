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

# 1. Create Project Hub (without formula first)
project_hub_props = {
    "Name": {"title": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "🔴 進行中", "color": "red"},
                {"name": "🟡 測試中", "color": "yellow"},
                {"name": "🟢 已部署", "color": "green"},
                {"name": "⚪ 暫緩", "color": "gray"}
            ]
        }
    },
    "Category": {
        "select": {
            "options": [
                {"name": "System Dev", "color": "blue"},
                {"name": "DevOps", "color": "purple"},
                {"name": "Procurement", "color": "orange"},
                {"name": "Infra", "color": "brown"}
            ]
        }
    }
}

print("Creating Project Hub...")
project_hub = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "title": [{"type": "text", "text": {"content": "📂 Project Hub (核心專案庫)"}}],
    "properties": project_hub_props
})

if project_hub:
    project_hub_id = project_hub["id"]
    
    # 2. Create Daily Matrix (establish relation)
    daily_matrix_props = {
        "Action": {"title": {}},
        "Priority": {
            "select": {
                "options": [
                    {"name": "P1-Critical", "color": "red"},
                    {"name": "P2-High", "color": "orange"},
                    {"name": "P3-Normal", "color": "blue"}
                ]
            }
        },
        "Execution Date": {"date": {}},
        "Status": {"checkbox": {}},
        "Tech Debt": {
            "multi_select": {
                "options": [
                    {"name": "Legacy_Fix", "color": "yellow"},
                    {"name": "System_Bug", "color": "red"},
                    {"name": "Optimizing", "color": "green"}
                ]
            }
        },
        "Project Hub": {
            "relation": {
                "database_id": project_hub_id,
                "type": "dual_property",
                "dual_property": {"synced_property_name": "Daily Matrix"}
            }
        }
    }
    print("Creating Daily Matrix...")
    daily_matrix = notion_request("databases", "POST", {
        "parent": {"type": "page_id", "page_id": PAGE_ID},
        "title": [{"type": "text", "text": {"content": "📝 Daily Matrix (矩陣行動清單)"}}],
        "properties": daily_matrix_props
    })

    if daily_matrix:
        # 3. Now add the Formula to Project Hub
        print("Adding progress formula to Project Hub...")
        notion_request(f"databases/{project_hub_id}", "PATCH", {
            "properties": {
                "Digital Progress": {
                    "formula": {
                        "expression": 'let(done, prop("Daily Matrix").filter(current.prop("Status")).length(), total, prop("Daily Matrix").length(), percent, if(total > 0, done / total, 0), bar, slice("▓▓▓▓▓▓▓▓▓▓", 0, round(percent * 10)) + slice("░░░░░░░░░░", 0, 10 - round(percent * 10)), bar + " " + format(round(percent * 100)) + "%")'
                    }
                }
            }
        })

        # 4. Create Intel & Ideas
        intel_props = {
            "Intel": {"title": {}},
            "Source": {
                "select": {
                    "options": [
                        {"name": "Web", "color": "blue"},
                        {"name": "Chat", "color": "green"},
                        {"name": "Brainstorm", "color": "purple"},
                        {"name": "OpenClaw", "color": "orange"}
                    ]
                }
            },
            "Weight": {
                "select": {
                    "options": [
                        {"name": "⭐"}, {"name": "⭐⭐"}, {"name": "⭐⭐⭐"}, {"name": "⭐⭐⭐⭐"}, {"name": "⭐⭐⭐⭐⭐"}
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "gray"},
                        {"name": "Researching", "color": "yellow"},
                        {"name": "To-Project", "color": "green"}
                    ]
                }
            },
            "Incubation": {
                "relation": {
                    "database_id": project_hub_id,
                    "type": "single_property",
                    "single_property": {}
                }
            }
        }
        print("Creating Intel & Ideas...")
        intel = notion_request("databases", "POST", {
            "parent": {"type": "page_id", "page_id": PAGE_ID},
            "title": [{"type": "text", "text": {"content": "💡 Intel & Ideas (靈感與技術情報)"}}],
            "properties": intel_props
        })

        # 5. Create Dashboard Layout
        print("Setting up Dashboard layout...")
        notion_request(f"blocks/{PAGE_ID}/children", "PATCH", {
            "children": [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": "> [ SYSTEM STATUS: ONLINE ] | NODE: ZEABUR-G928 | USER: MANAGER_GHIEN"}}],
                        "icon": {"emoji": "⚡"},
                        "color": "gray_background"
                    }
                }
            ]
        })
        
        print("Setup complete.")
    else:
        print("Failed to create Daily Matrix.")
else:
    print("Aborting setup due to Project Hub creation failure.")
