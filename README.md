# SDD-Demo

本專案為 Spec‑Driven Development（SDD）示範範例，示範使用 `specify` 工具與 AI Agent workflow 來建立需求、檢查清單與發佈流程。

## 主要功能

本專案實作了一個程式版本發佈通知系統（Release Announcements），包含以下功能：

- 建立發佈草稿與預覽郵件內容
- 選擇收件人並執行同步郵件發送
- 管理收件人與程式清單
- 檢視發送紀錄與稽核
- 開發環境 SMTP 模擬與測試

## 快速開始

### 1. 建立並啟用虛擬環境

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 2. 安裝相依套件

```bash
cd backend
pip install -r requirements.txt
```

### 3. 設定環境變數

複製 `.env.example` 為 `.env` 並設定必要變數：

```bash
cp backend/.env.example backend/.env
# 編輯 .env 檔案設定 SMTP 與資料庫連線
```

### 4. 初始化資料庫

```bash
cd backend
# 如果使用 Alembic
alembic upgrade head

# 或直接啟動應用程式會自動建立資料表
```

### 5. 啟動開發伺服器

```bash
cd backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

訪問 http://localhost:8000/docs 查看 API 文件。

### 6. 執行測試

```bash
cd backend
pytest -v
```

## 詳細文件

- **開發者快速指引**: [Docs/DEVELOPER_QUICKSTART.md](Docs/DEVELOPER_QUICKSTART.md)
- **功能規格**: [specs/001-release-announcements/spec.md](specs/001-release-announcements/spec.md)
- **實作計畫**: [specs/001-release-announcements/plan.md](specs/001-release-announcements/plan.md)
- **資料模型**: [specs/001-release-announcements/data-model.md](specs/001-release-announcements/data-model.md)
- **API 使用範例**: [specs/001-release-announcements/quickstart.md](specs/001-release-announcements/quickstart.md)
- **任務清單**: [specs/001-release-announcements/tasks.md](specs/001-release-announcements/tasks.md)

## 專案結構

```
SDD-Demo/
├── backend/              # 後端 API 服務
│   ├── api/             # API 路由
│   ├── models.py        # 資料模型
│   ├── schemas.py       # Pydantic Schemas
│   ├── auth.py          # 授權中介層
│   ├── emailer.py       # 郵件發送
│   ├── config.py        # 設定管理
│   └── tests/           # 測試
├── specs/               # 功能規格文件
│   └── 001-release-announcements/
├── Docs/                # 專案文件
└── .github/workflows/   # CI/CD 設定
```

## 技術堆疊

- **語言**: Python 3.11+
- **框架**: FastAPI
- **資料庫**: SQLite (MVP) / PostgreSQL (生產)
- **ORM**: SQLAlchemy
- **測試**: pytest
- **郵件**: SMTP (標準庫)

## 貢獻

本專案遵循 Spec-Driven Development 流程：

1. 先建立完整的功能規格 (`spec.md`)
2. 通過規格檢查表驗證 (`checklists/`)
3. 制定實作計畫 (`plan.md`)
4. 分解任務清單 (`tasks.md`)
5. 按階段執行實作

詳情請參閱 [AGENTS.md](AGENTS.md)。

## 模型選擇

* GPT‑4.1 / GPT‑4o / GPT‑5 mini 使用筆記

### 一句話總結

平常 Speckit 規格＋寫程式建議預設用 **GPT‑4.1（0x）**，需要看圖時改用 **GPT‑4o**，遇到特別複雜或超大專案再短暫切到 **GPT‑5 mini**。

### 模型比較總覽

| 模型        | 建議優先度 | 特性重點 | 典型用途 |
|------------|------------|----------|----------|
| GPT‑4.1    | ★★★★☆（首選） | 推理與程式能力佳、速度夠快、成本合理，官方與多方測試都把它當通用預設工作馬。| 日常 Speckit 規格撰寫、一般系統設計、程式生成與重構、高頻互動。 |
| GPT‑4o     | ★★★☆☆        | 多模態能力強，支援影像輸入；文字與程式推理略遜於 4.1，但延遲低、體驗順。| 需要讀圖（流程圖、UI 截圖）、簡報截圖轉規格或程式的情境。 |
| GPT‑5 mini | ★★★★☆（進階用） | GPT‑5 家族的精簡版，比 4.1/4o 更聰明、上下文更大，但延遲與成本較高。 | 超長規格文件、跨多模組架構設計、困難 bug root cause 分析、大型專案一次性檢視。 |

### 為何 GPT‑4.1 適合作為預設

- GPT‑4.1 在程式理解、長上下文推理與回應品質上，普遍被評為優於 GPT‑4o，同時維持相近甚至更好的成本效益與延遲表現。
- 文件與 Copilot 指南也將 GPT‑4.1 視為通用預設模型，特別適合高頻、需要即時回饋的開發與寫作工作流程。

### 什麼時候改用 GPT‑4o

- 任務需要處理圖片（如系統架構圖、UI 截圖、筆記照相）並轉成文字描述或程式碼時，GPT‑4o 的多模態能力更合適。 
- 對於只是一般文字規格與程式開發，4.1 在推理與程式相關基準測試上通常略勝 4o，若沒有影像需求就不需要特別切換。

### 什麼時候考慮 GPT‑5 mini

- GPT‑5 系列在複雜推理、困難程式挑戰、多模態理解等基準上，整體表現優於 4.1 與 4o，mini 版本提供較佳的成本與速度折衷。 
- 適合處理一次要讀很多檔的大型 SDD/ADR、複雜架構評估、或長期追查難以重現的錯誤；但因成本與延遲較高，不建議當作每天高頻 Speckit 指令與一般 coding 的預設模型。
