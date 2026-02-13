import os
import json
import urllib.request

TOKEN = os.environ.get("NOTION_TOKEN")
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

# Black Ops Triage Logic
print("Starting Black Ops Triage...")

tasks = [
    {
        "title": "1. 晨間簡報：抓取天氣/日曆/TODO，每日 08:00 推播摘要。",
        "time": 20, "energy": "🔋低能", "moscow": "Should",
        "dod": "完成 weather/calendar 串接，並在 TG 收到格式正確的晨間摘要。",
        "risk": "API 額度超限 -> 設定監控警告"
    },
    {
        "title": "2. GitHub 趨勢：定時搜尋 AI 專案並摘要推播。",
        "time": 45, "energy": "⚡️高能", "moscow": "Must",
        "dod": "成功自動過濾重複專案，並推送至少 3 個高品質 AI 專案至 TG。",
        "risk": "搜尋結果噪音過多 -> 優化關鍵字過濾"
    },
    {
        "title": "3. 社群哨兵：心跳監測 X/Threads 關鍵字，過濾廢話。",
        "time": 30, "energy": "⚡️高能", "moscow": "Could",
        "dod": "能識別並排除廣告推文，回報真實的技術討論。",
        "risk": "網頁結構變動 -> 需定期校準爬蟲"
    },
    {
        "title": "4. 郵件秘書：讀取 Gmail 並分類摘要，產出回覆草稿。",
        "time": 60, "energy": "⚡️高能", "moscow": "Should",
        "dod": "AI 成功分類為緊急/一般，並產出語氣正確的建議回覆。",
        "risk": "隱私外洩風險 -> 確保僅處理公開工作郵件"
    },
    {
        "title": "5. 成本守門員：每 4 小時監控 Token 消耗並預警。",
        "time": 15, "energy": "🔋低能", "moscow": "Must",
        "dod": "每 4 小時準時在 TG 收到回報，超標時發出紅色警報。",
        "risk": "監控程序當機 -> 加入外部監測 (Zeabur)"
    },
    {
        "title": "6. 記憶維護：夜間提煉對話精華更新 MEMORY.md。",
        "time": 30, "energy": "⚡️高能", "moscow": "Must",
        "dod": "MEMORY.md 自動更新當日重大決策，無冗餘廢話。",
        "risk": "遺漏重要細節 -> 加強語意識別 Prompt"
    },
    {
        "title": "7. 專案看板：檢查 git/檔案狀態，自動更新進度條。",
        "time": 40, "energy": "⚡️高能", "moscow": "Should",
        "dod": "Notion 專案進度條與實際 GitHub Commit 狀態同步。",
        "risk": "Token 權限不足 -> 使用最小必要權限 Repo Token"
    },
    {
        "title": "8. 訊息整理：每日彙整特定群組技術精華。",
        "time": 25, "energy": "🔋低能", "moscow": "Could",
        "dod": "產出精簡的 Bullet Points，讀完不超過 3 分鐘。",
        "risk": "訊息量爆炸導致 Token 溢出 -> 實施分段處理"
    },
    {
        "title": "9. 智慧提醒：根據對話意圖動態建立提醒任務。",
        "time": 20, "energy": "⚡️高能", "moscow": "Should",
        "dod": "說出 '記得提醒我...' 後，系統自動在 Cron 列表新增任務。",
        "risk": "誤判提醒意圖 -> 增加二次確認機制"
    },
    {
        "title": "10. 深夜研究：深度主題搜尋並產出研究文檔。",
        "time": 90, "energy": "⚡️高能", "moscow": "Must",
        "dod": "產出包含目錄、數據、趨勢分析的 1000 字以上 Markdown 文件。",
        "risk": "深度不足 -> 實施多輪多代理搜尋 (Iterative Search)"
    },
    {
        "title": "11. 系統健檢：監控伺服器狀態，異常時報警。",
        "time": 15, "energy": "🔋低能", "moscow": "Must",
        "dod": "當 Zeabur 服務 Crash 時，1 分鐘內在 TG 收到告警。",
        "risk": "告警通道阻塞 -> 設定雙重告警機制 (Email+TG)"
    },
    {
        "title": "12. 任務委派：主從架構分工執行複雜任務。",
        "time": 45, "energy": "⚡️高能", "moscow": "Should",
        "dod": "成功 Spawn 子 Agent 處理子任務，並回傳匯總結果。",
        "risk": "子 Agent 跑飛失控 -> 設定最大運行限制與預算"
    },
    {
        "title": "13. 行事曆助理：分析行程衝突與距離，預警提示。",
        "time": 30, "energy": "🔋低能", "moscow": "Could",
        "dod": "行程衝突時主動跳出 Alert 並建議調整方案。",
        "risk": "隱私權限過大 -> 僅讀取工作日曆標題與時間"
    },
    {
        "title": "14. 晚安回顧：總結今日產出並確認明日計畫。",
        "time": 15, "energy": "🔋低能", "moscow": "Should",
        "dod": "23:00 準時產出今日任務達成率報告。",
        "risk": "遺漏手動更新事項 -> 比對 Notion 最後修改時間"
    }
]

# Get existing page IDs for these tasks
results = notion_request(f"data_sources/{GTD_TASKS_DS_ID}/query", "POST")
id_map = {p["properties"]["⚡ 行動指令"]["title"][0]["text"]["content"]: p["id"] for p in results["results"]}

combat_targets = ["10. 深夜研究", "6. 記憶維護", "5. 成本守門員"] # Selected today's combat tasks

for t in tasks:
    page_id = id_map.get(t["title"])
    if not page_id: continue
    
    print(f"Updating: {t['title']}")
    is_combat = any(target in t["title"] for target in combat_targets)
    
    properties = {
        "📊 狀態": {"select": {"name": "Next Action"}},
        "📥 快速捕捉": {"checkbox": False},
        "⚔️ 衝刺狀態": {"status": {"name": "In Progress" if is_combat else "Backlog"}},
        "📌 MoSCoW": {"select": {"name": t["moscow"]}},
        "🔋 能量等級": {"select": {"name": t["energy"]}},
        "⏱️ 預估時間(分鐘)": {"number": t["time"]},
        "✅ DoD": {"rich_text": [{"text": {"content": t["dod"]}}]},
        "☠️ Pre-mortem Risk": {"rich_text": [{"text": {"content": t["risk"]}}]}
    }
    
    if is_combat:
        from datetime import date
        properties["🗓️ 執行日期"] = {"date": {"start": date.today().isoformat()}}
        
    notion_request(f"pages/{page_id}", "PATCH", {"properties": properties})

print("Black Ops Triage Completed.")
