
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

### 釐清需求

* 釐清需求 1

  ```bash
  /speckit.clarify 
  ``` 
  - Q1: 認證方式應採何種方式？ → A: 使用簡易 email/password 登入並以伺服器端 Session 管理（短期方案，未來可升級為 JWT/SSO）。
  - Q2: 發送方式要採同步或非同步？ → A: 同步直接發送（透過 SMTP），API 呼叫會等候 SMTP 回應並回傳成功或失敗。
  - Q3: 單次發佈預期最大收件人量為多少？ → A: 單次上限設為 <= 500 收件人（若超過需採分批或升級為非同步架構）。
  - Q4: 同步發送時是否執行自動重試或重發機制？ → A: 否，採單次 SMTP 嘗試；系統預期使用者管理之收件地址均為有效，系統不做自動重試或回滾，僅記錄每位收件人的結果。
  - Q5: 同步發送 API 最長等待 SMTP 回應的 timeout 要多少？ → A: API 同步發送 timeout 設為 30 秒（短期上限，避免長時間阻塞）。
  - Q6: 是否在 MVP 驗證 "成功送達率 >= 98%"（SC-002）？ → A: 否。由使用者管理收件對象，MVP 不需驗證發送成功率或模擬失敗率。
