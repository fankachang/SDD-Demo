# Research — 技術決策紀錄

下面為本 feature 在 Phase 0 的所有 NEEDS CLARIFICATION 條目已解決之決策、理由與考慮的替代方案。

---

Decision: Language/Runtime — Python 3.14

Rationale:
- 使用者環境為 Python 3.14 的虛擬環境；更新決策以配合實際開發環境，降低環境差異成本。
- Python 生態（FastAPI, SQLAlchemy, pytest）在 3.14 上可正常運行，能快速建置小型 Web 後端並與 SMTP/SQLite 整合，適合 MVP。

Alternatives considered:
- Node.js (Express/Fastify)：同樣適合，但現有環境顯示 Python 開發虛擬環境，選 Python 可減少環境調整成本。
- Go/Rust：效能佳但開發成本與範例較高，不符合 MVP 最小化原則。

---

Decision: Primary Dependencies — FastAPI, SQLAlchemy, Alembic, Jinja2, stdlib `smtplib`

Rationale:
- FastAPI 提供快速建立 REST API、良好測試支援與自動文件（OpenAPI）。
- SQLAlchemy + Alembic 可在 SQLite 上快速建立可遷移的資料模型，且後續能比較容易切換到 PostgreSQL。
- Jinja2 用於郵件模板渲染（簡單且熟悉）。
- 同步 SMTP 使用 Python 標準庫 `smtplib` 達成規格中「同步直接發送（透過 SMTP）」的要求，避免一開始就引入外部依賴或佇列系統。

Alternatives considered:
- 使用外部郵件服務（SendGrid、Mailgun）：可提高可靠性，但需憑證與第三方帳戶設定，超出 MVP 範圍。
- 非同步郵件佇列（Celery、RQ、Sidekiq）：為未來擴充選項；當前規格要求同步 API 行為，僅在後端背景工作中作為延伸。

---

Decision: Storage — SQLite (MVP)

Rationale:
- 輕量、免設定，適合本地開發與自動化測試。
- 資料模型用標準 SQLAlchemy 設計，未來能無痛遷移到 PostgreSQL。

Alternatives considered:
- 直接使用 PostgreSQL：生產上優先，但增加開發/CI 設定負擔；可在部署階段改用 PostgreSQL。

---

Decision: Testing — pytest

Rationale:
- Python 預設測試工具選擇，廣泛支援 FastAPI 與 SQLAlchemy 的測試模式。

Alternatives considered:
- unittest：可用但較冗長；pytest 提供簡潔的 fixture 與插件生態。

---

Decision: Target Platform & Project Type — Linux server (container-ready), Web backend

Rationale:
- 後端服務屬 Web API，部署於 Linux 容器或 Linux VM 是常見選擇；本地開發以 macOS 支援。

Alternatives considered:
- Serverless：初期不採用，以降低複雜度與依賴。

---

Decision: Performance Goals / Constraints

Rationale & Decisions:
- 支援同步發送上限為單次 <= 500 收件人（由需求指定）。
- 同步發送 API timeout 設為 30 秒，超時回傳錯誤並在 `send_logs` 記錄超時情況。
- 查詢歷史紀錄的目標回應時間 < 2 秒（在可預期的資料量下）。

Alternatives considered:
- 立即導入非同步/分批發送以支援更大收件量；設計上保留為未來擴充，但不在 MVP 實作以避免過度設計。

---

- Summary / Next Steps

- 以 Python 3.14 + FastAPI + SQLite 為 MVP 技術基線。
- 採用標準同步 SMTP（`smtplib`）實作同步發送 API；如需更高可靠性，再提出將非同步佇列或外部郵件供應商納入的實作提案。
- Phase 1 將根據此決策產出 `data-model.md`、API contracts（OpenAPI）與 `quickstart.md`。

