# SDD Flow Test Project

* Init specify

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

* 修改 AGENTS.md

```bash
* Except for the constitution, which MUST be in English, all specifications, agreements, and user-oriented documents MUST be written in Traditional Chinese (zh-TW).
* When drafting the constitution, the context MUST be translated into "constitution_zhTW.md" and placed in the same directory (please note that file names are case-sensitive).
* Git Log, Code annotations MUST be written in Traditional Chinese (zh-TW)
```

* 新增憲法文件

* 追加規則

```bash
/speckit.constitution  不要過度開發也不要過度設計
```