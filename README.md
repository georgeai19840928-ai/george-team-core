# George Team Core (george-team-core) 🦐✨

這是「蝦蝦戰隊」的核心工具庫，專門存放團隊運行的自動化腳本、核心研發引擎以及長期記憶日誌。

## 🎯 專案目標
1. **透明化開發**：讓老闆隨時能查閱喬治蝦與程式蝦的代碼實作。
2. **模組化工具**：封裝 Notion 自動化、系統監控等重複使用的功能。
3. **知識持久化**：確保開發決策與對話精華有版本控制。

## 🏗️ 系統架構

```text
george-team-core/
├── src/
│   ├── notion/         # Notion 自動化工作流 (Triage, Hydration, Logs)
│   ├── researcher/     # DEEP_RESEARCH_MODE 核心搜尋與分析引擎
│   └── utils/          # 共用工具 (Environment, Telegram Notify)
├── memory/             # 每日對話精華日誌備份 (Markdown)
├── docs/               # 技術規格與協議文檔
└── scripts/            # 部署與維修用一次性腳本
```

## 🛠️ 目前核心模組規格

### 1. Notion 自動化 [src/notion/]
- **Triage Protocol**: 實現 GTD Inbox 自動分流邏輯。
- **Hydration Engine**: 自動在專案頁面插入原子任務實體連結。
- **Intel Distiller**: 每日凌晨 03:00 自動提煉對話並寫入 DAILY_INTEL_LOGS。

### 2. Deep Research Engine [src/researcher/]
- **Iterative Search**: 多步遞迴搜尋邏輯，根據初步結果深入探索。
- **Content Cleaner**: 清理爬取的 HTML 內容，轉為純淨 Markdown。
- **Synthesis Prompt**: 針對 1000 字以上報告設計的分析 Prompt。

## 📡 運行環境
- **Runtime**: Python 3.11+ / Node.js (OpenClaw)
- **Deployment**: Zeabur
- **Connectors**: Notion API, GitHub API, Telegram Bot API

---
*Created by George Shrimp (@G928_Sigma_bot) for George Ghien.*
