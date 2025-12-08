
## 操作紀錄（轉移自 README.md）

### speckit 初始化

```bash
> specify init .

                        ███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗                        
                        ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝                        
                        ███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝                         
                        ╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝                          
                        ███████║██║     ███████╗╚██████╗██║██║        ██║                           
                        ╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝                           
                                                                                                    
                         GitHub Spec Kit - Spec-Driven Development Toolkit                          

Warning: Current directory is not empty (3 items)
Template files will be merged with existing content and may overwrite existing files
Do you want to continue? [y/N]: y
╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                  │
│  Specify Project Setup                                                                           │
│                                                                                                  │
│  Project         SDD-Demo                                                                        │
│  Working Path    /Users/fanka/AIProject/SDD-Demo                                                 │
│                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────── Choose your AI assistant: ────────────────────────────────────╮
│                                                                                                  │
│  ▶      copilot (GitHub Copilot)                                                                 │
│         claude (Claude Code)                                                                     │
│         gemini (Gemini CLI)                                                                      │
│         cursor (Cursor)                                                                          │

Selected AI assistant: copilot
Selected script type: sh
Initialize Specify Project
├── ● Check required tools (ok)
Initialize Specify Project
├── ● Check required tools (ok)
├── ● Select AI assistant (copilot)
├── ● Select script type (sh)
├── ● Fetch latest release (release v0.0.90 (59,640 bytes))
├── ● Download template (spec-kit-template-copilot-sh-v0.0.90.zip)
├── ● Extract template
├── ● Archive contents (39 entries)
├── ● Extraction summary (temp 3 items)
├── ● Ensure scripts executable (5 updated)
├── ● Cleanup
├── ● Initialize git repository (existing repo detected)
└── ● Finalize (project ready)

Project ready.

Release v1.0.1 created for constitution metadata updates.

╭───────────────────────────────────── Agent Folder Security ──────────────────────────────────────╮
│                                                                                                  │
│  Some agents may store credentials, auth tokens, or other identifying and private artifacts in   │
│  the agent folder within your project.                                                           │
│  Consider adding .github/ (or parts of it) to .gitignore to prevent accidental credential        │
│  leakage.                                                                                        │
│                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────── Next Steps ───────────────────────────────────────────╮
│                                                                                                  │
│  1. You're already in the project directory!                                                     │
│  2. Start using slash commands with your AI agent:                                               │
│     2.1 /constitution - Establish project principles                                             │
│     2.2 /specify - Create baseline specification                                                 │
│     2.3 /plan - Create implementation plan                                                       │
│     2.4 /tasks - Generate actionable tasks                                                       │
│     2.5 /implement - Execute implementation                                                      │
│                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────── Enhancement Commands ──────────────────────────────────────╮
│                                                                                                  │
│  Optional commands that you can use for your specs (improve quality & confidence)                │
│                                                                                                  │
│  ○ /clarify (optional) - Ask structured questions to de-risk ambiguous areas before planning     │
│  (run before /plan if used)                                                                      │
│  ○ /analyze (optional) - Cross-artifact consistency & alignment report (after /tasks, before     │
│  /implement)                                                                                     │
│                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
> 
```
### 建立 AGENTS.md

* 重要設定與規範
  - Agents 規範：請參考 AGENTS.md（部分重要原則如下）：
    - 除憲法（constitution）外，所有 specs、合約、與面向使用者的文件均使用繁體中文（zh-TW）。
    - 憲法檔案請以英文撰寫；並在同目錄產生對應的繁體中文翻譯檔 `constitution_zhTW.md`。
    - Git 提交訊息與程式碼註解請使用繁體中文。

* AGENTS.md 內容

  ```bash
  * Except for the constitution, which MUST be in English, all specifications, agreements, and user-oriented documents MUST be written in Traditional Chinese (zh-TW).
  * When drafting the constitution, the context MUST be translated into "constitution_zhTW.md" and placed in the same directory (please note that file names are case-sensitive).
  * Git Log, Code annotations MUST be written in Traditional Chinese (zh-TW)
  ```
### 需求文件建立

* 以下操作皆用 Bast Agent 3.1 + Raptor mini Model 進行
* 當執行 /speckit.* 指令時 Agent 會自行跳轉至該指令的 Agent
* 常見工作流程（範例）
  1. 使用 `/specify` 產生需求骨架，例如建立 `Docs/需求說明.md`。
  2. 使用 `/clarify` 釐清需求細節（Q&A）並更新規格檔案。
  3. 使用 `/speckit.checklist` 產生需求品質檢查清單並與 `specs` 下的 `requirements.md` 合併。
  4. 使用 `/plan` 與 `/implement` 生成與執行任務清單。

* 範例內容（已產生）
  ```bash
  請幫我寫一個需求的 prompt:
  建立一個程式版本發佈網站，主要功能為當程式發佈時需要發信給特定使用者的公告信件

  流程：
  一、步驟1：輸入以下項目：

  發佈程式名稱◊
  發佈程式版本
  使用者配合事項
  二、步驟2：檢視要發佈的內容
  三、將檢視的內容發送給特定使用者

  四、需要後檯管理介面，需具備功能：

  收件人信箱管理（具體要發給哪些使用者，需要可設定 CC or BCC）
  需要可以設定 發佈程式列表
  ```


* 上述產生的檔案/目錄
  - Docs/需求說明.md — 需求說明草稿
  - specs/001-release-announcements/ — 範例規格與檢查清單（requirements.md、requirements-qa.merged.md 等）
  - AGENTS.md — Agent 規則與指引

* 需求確認

```bash
/speckit.specify  #file:需求說明.md 
```

### 釐清需求

* 釐清需求

  ```bash
  /speckit.clarify 

  - Q1: Recommended: Option [B] - 以後端背景任務排程重試，可降低同步請求風險並利於擴充、觀察與重試控制。

    Option	Description
    A	在 UI 中允許對單一收件人即時手動重發（同步操作）
    B	提供伺服器端「重試/重發」背景工作（排入佇列，由後端非同步處理）
    C	MVP 不提供重發功能，只記錄失敗供稽核（不自動/手動重發）
    Short	其他（短答 <=5 字）
  ```
  > B
  ```bash
  已更新檔案： spec.md
  進度

    * 問題數：1（已問並記錄）
    * TODO 更新：掃描規格檔不明確處 已完成，逐一提問並整合答覆 進行中。

  建議下一步：執行 /speckit.plan 以把已釐清的需求拆成實作任務與排程。是否要我現在開始產生實作計畫？
  ``` 
