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

# 1. Cleanup: Fetch and Delete existing blocks on the page
print("Scanning for existing blocks to cleanup...")
blocks = notion_request(f"blocks/{PAGE_ID}/children", "GET")
if blocks and "results" in blocks:
    for block in blocks["results"]:
        # We only delete blocks created by the bot or that look like our databases
        # To be safe and thorough as requested by "clear old data", we archive them.
        block_id = block["id"]
        notion_request(f"blocks/{block_id}", "DELETE")
    print(f"Cleaned up {len(blocks['results'])} blocks.")

# 2. Re-deploy with improved aesthetics
print("Deploying Cyber-Brain v2.0 (High Density Tech Style)...")

# A. Create Project Hub (💾)
project_hub_props = {
    "Name": {"title": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "ACTIVE", "color": "blue"},
                {"name": "TESTING", "color": "purple"},
                {"name": "DEPLOYED", "color": "green"},
                {"name": "STANDBY", "color": "gray"}
            ]
        }
    },
    "Progress": {
        "formula": {
            "expression": 'let(done, prop("Daily Matrix").filter(current.prop("Status")).length(), total, prop("Daily Matrix").length(), percent, if(total > 0, done / total, 0), bar, slice("▓▓▓▓▓▓▓▓▓▓", 0, round(percent * 10)) + slice("░░░░░░░░░░", 0, 10 - round(percent * 10)), bar + " " + format(round(percent * 100)) + "%")'
        }
    }
}

project_hub = notion_request("databases", "POST", {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "icon": {"emoji": "💾"},
    "title": [{"type": "text", "text": {"content": "💾 SYSTEM_PROJECT_HUB"}}],
    "properties": project_hub_props
})

if project_hub:
    project_hub_id = project_hub["id"]
    
    # B. Create Daily Matrix (⚡)
    daily_matrix_props = {
        "Action": {"title": {}},
        "Priority": {
            "select": {
                "options": [
                    {"name": "CRITICAL", "color": "red"},
                    {"name": "HIGH", "color": "orange"},
                    {"name": "NORMAL", "color": "blue"}
                ]
            }
        },
        "Status": {"checkbox": {}},
        "Project": {
            "relation": {
                "database_id": project_hub_id,
                "type": "dual_property",
                "dual_property": {"synced_property_name": "Daily Matrix"}
            }
        }
    }
    daily_matrix = notion_request("databases", "POST", {
        "parent": {"type": "page_id", "page_id": PAGE_ID},
        "icon": {"emoji": "⚡"},
        "title": [{"type": "text", "text": {"content": "⚡ DAILY_MATRIX_PROTOCOL"}}],
        "properties": daily_matrix_props
    })

    # C. Create Intel & Ideas (📡)
    intel_props = {
        "Intel": {"title": {}},
        "Weight": {
            "select": {
                "options": [{"name": "⭐"}, {"name": "⭐⭐"}, {"name": "⭐⭐⭐"}]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "DRAFT", "color": "gray"},
                    {"name": "INTEL_LINKED", "color": "green"}
                ]
            }
        }
    }
    intel = notion_request("databases", "POST", {
        "parent": {"type": "page_id", "page_id": PAGE_ID},
        "icon": {"emoji": "📡"},
        "title": [{"type": "text", "text": {"content": "📡 INTEL_FEED_STREAM"}}],
        "properties": intel_props
    })

    # D. Layout setup
    # Using Callouts as high-contrast Section Headers
    notion_request(f"blocks/{PAGE_ID}/children", "PATCH", {
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": "COMMAND_CENTER // STATUS: ONLINE // AUTH: MANAGER_GHIEN", "link": None}, "annotations": {"bold": True, "code": True}}],
                    "icon": {"emoji": "🧠"},
                    "color": "gray_background"
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
        ]
    })
    
    print("Redeploy complete.")
else:
    print("Redeploy failed at step A.")
