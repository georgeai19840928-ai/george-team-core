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

# 1. Cleanup Duplicate Projects
print("Cleaning duplicate projects...")
duplicate_project_id = "30652d88-a5a9-812d-bdff-c7fe61d1d609"
notion_request(f"pages/{duplicate_project_id}", "PATCH", {"archived": True})

# 2. Cleanup Tasks linked to the duplicate project
print("Cleaning tasks linked to duplicate project...")
query = notion_request(f"data_sources/{GTD_TASKS_DS_ID}/query", "POST", {
    "filter": {
        "property": "🔗 所屬專案",
        "relation": {"contains": duplicate_project_id}
    }
})
if query and "results" in query:
    for page in query["results"]:
        notion_request(f"pages/{page['id']}", "PATCH", {"archived": True})

# 3. Cleanup Duplicate 14 Functions (if any left)
print("Checking for duplicate task titles...")
all_tasks = notion_request(f"data_sources/{GTD_TASKS_DS_ID}/query", "POST")
seen_titles = set()
if all_tasks and "results" in all_tasks:
    for page in all_tasks["results"]:
        title_list = page["properties"]["⚡ 行動指令"]["title"]
        if not title_list: continue
        title = title_list[0]["text"]["content"]
        if title in seen_titles:
            print(f"Archiving duplicate task: {title}")
            notion_request(f"pages/{page['id']}", "PATCH", {"archived": True})
        else:
            seen_titles.add(title)

# 4. Enhance Project Pages with Linked Views
# Note: Creating linked database views via API is limited. 
# We can append a paragraph with a link or instructions.
# Actually, we can add a 'Synced Block' or just 'Link to Page' if they were sub-pages.
# But since they are relations, the best we can do is add a heading.

projects = [
    {"id": "30652d88-a5a9-8122-8d1f-f888f2955aed", "name": "🦐 數位員工核心功能開發"},
    {"id": "30652d88-a5a9-8117-bfcf-efdbbd494b34", "name": "[ENGINE-01] DEEP_RESEARCH_MODE"}
]

for p in projects:
    print(f"Enhancing project page: {p['name']}")
    notion_request(f"blocks/{p['id']}/children", "PATCH", {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📋 任務清單 (Related Tasks)"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "此區域建議在 Notion UI 中手動建立一個 'Linked View of Database'，並過濾此專案的任務。API 目前無法直接建立視圖。"}}] }
            }
        ]
    })

print("Cleanup and Enhancement Complete.")
