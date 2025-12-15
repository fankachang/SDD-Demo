---
description: "Task list for 001-release-announcements"
---

# Tasks: 程式版本發佈（Release Announcements）

注意：本檔以繁體中文撰寫，任務以能直接執行的清單格式列出，並以使用者故事為主要組織單位。

Feature 資料夾：`/specs/001-release-announcements`

## Phase 1: Setup（專案初始化）

- [X] T001 建立並確認開發虛擬環境與相依檔案（`backend/requirements.txt`）
- [X] T002 [P] 在 `backend/` 中建立或確認基本檔案：`backend/main.py`, `backend/db.py`, `backend/models.py`, `backend/schemas.py`, `backend/emailer.py`
- [X] T003 [P] 新增環境範本檔案 `backend/.env.example` 並記載必要環境變數（`SMTP_HOST` 等）
- [X] T004 新增或更新 `specs/001-release-announcements/tasks.md`（本檔）並提交版本控制
- [X] T005 [P] 在 repo 根目錄更新 README 或 quickstart 引導：`specs/001-release-announcements/quickstart.md`

## Phase 2: Foundational（基礎建置 — 必須完成以解鎖各使用者故事）

- [X] T006 設計並在 `backend/models.py` 中建立核心資料模型：`User`, `Program`, `Contact`, `Release`, `ReleaseRecipient`, `SendLog`（依據 `specs/001-release-announcements/data-model.md`）
- [X] T007 建立 `backend/db.py` 的資料庫初始化與 session 管理函式，並在 `backend/alembic/` 初始化 migration（若採 Alembic，提供 migration 設定檔路徑）
- [X] T008 [P] 在 `backend/schemas.py` 實作 Pydantic schema（或 Pydantic v2 的 ConfigDict）對應於 models：`UserSchema`, `ProgramSchema`, `ContactSchema`, `ReleaseCreateSchema`, `RecipientInputSchema`, `SendLogSchema`
- [X] T009 實作簡易授權中介層 `backend/auth.py`（email/password 登入與 session 管理的 skeleton），並在 `backend/main.py` 註冊中介層
- [X] T010 在 `backend/emailer.py` 實作同步 SMTP 抽象（`send_email(to_list, cc, bcc, subject, body, timeout=30)`），並支援透過環境變數切換到本機模擬 SMTP
- [X] T011 在 `backend/main.py` 設定 API 路由註冊點與錯誤處理 middleware（含 400/504 處理邏輯）
- [X] T012 新增 logging 與環境設定載入 `backend/config.py`（讀取 `DATABASE_URL`、SMTP 設定等）

---

## Phase 3: User Story 1 - 建立發佈草稿與預覽 (Priority: P1)

Goal: 提供發佈者建立發佈草稿（程式、版本、說明）並在送出前看到郵件預覽。

Independent Test: 在 API 或 UI 呼叫建立 release 並呼叫 preview endpoint，可回傳渲染後郵件標題與內容。

- [X] T013 [P] [US1] 在 `backend/models.py` 補實作 `Release` 與 `ReleaseRecipient` 欄位與關聯（若尚未完全實作）
- [X] T014 [P] [US1] 在 `backend/schemas.py` 新增 `ReleaseCreateSchema` 與 `ReleasePreviewSchema`（包含 recipients 快照格式）
- [X] T015 [US1] 在 `backend/services/release_service.py`（建立新檔）實作 Release CRUD 與 preview 渲染方法（`render_release_preview(release_id)`）
- [X] T016 [US1] 在 `backend/api/releases.py`（建立新檔）實作路由：`POST /releases`（建立 draft）、`GET /releases/{id}/preview`（回傳渲染後內容）
- [X] T017 [US1] 在 `backend/templates/release_email.html` 新增郵件模板（Jinja2）以供預覽與發送使用
- [X] T018 [US1] 在 `backend/tests/test_release_preview.py`（建立新檔）加入整合測試：建立 release -> 呼叫 preview -> 驗證回傳包含標題與 body（若使用測試請求）
- [X] T019 [US1] 在 `backend/main.py` 註冊 `backend/api/releases.py` 路由與相依注入（database session, config）
- [X] T020 [US1] [P] 新增範例 API 呼叫範本於 `specs/001-release-announcements/quickstart.md`（示範建立並預覽 release 的 curl 或 HTTPie 範例）

---

## Phase 4: User Story 2 - 選擇收件人並發送 (Priority: P1)

Goal: 於步驟三選擇 To/CC/BCC 收件人並執行同步發送，回傳即時狀態並建立發送紀錄。

Independent Test: 呼叫 `POST /releases/{id}/send` 並提供 recipients，API 回傳逐位結果且 `SendLog` 產生紀錄。

 [X] T021 [P] [US2] 在 `backend/schemas.py` 新增 `RecipientInputSchema` 與 `SendResultSchema`
 [X] T022 [P] [US2] 在 `backend/services/mailer.py`（建立新檔）實作 `send_release_synchronously(release_id, recipients)`，使用 `backend/emailer.py` 的 send_email 並對每位收件人記錄結果
 [X] T023 [US2] 在 `backend/api/releases.py` 補實作 `POST /releases/{id}/send` endpoint，包含 recipients 數量檢查（>500 回 400）與 30 秒 timeout 行為（逾時回 504）
 [X] T024 [US2] 在 `backend/models.py` 新增或確認 `SendLog` 模型結構，並在發送完成後寫入紀錄
 [X] T025 [US2] 在 `backend/tests/test_send_flow.py` 新增測試：模擬 SMTP 成功/失敗情境，驗證 API 回傳格式與 `SendLog` 內容
 [X] T026 [US2] 在 `backend/api/releases.py` 的 send 路由中導入背景重試註記（非馬上實作背景重試，但記錄失敗以便後續 background retry 使用）
 [X] T027 [US2] 在 `backend/templates/` 加入針對發送結果的簡潔日誌範本（視需求可選）
 [X] T028 [US2] [P] 在 `specs/001-release-announcements/contracts/openapi.yaml` 中補強 `POST /releases/{id}/send` 的 request/response 範例（若需契約測試使用）

---

## Phase 5: User Story 3 - 收件人與程式清單管理 (Priority: P1)

Goal: 管理者能新增/編輯/刪除收件人與程式清單，變更即時反映於發佈表單選單。

Independent Test: 呼叫 Contacts / Programs 的 CRUD API，檢查在發佈建立時可選到更新後資料。

- [X] T029 [P] [US3] 在 `backend/api/contacts.py`（建立新檔）實作 `GET /contacts`, `POST /contacts`, `PUT /contacts/{id}`, `DELETE /contacts/{id}`
- [X] T030 [P] [US3] 在 `backend/api/programs.py`（建立新檔）實作 `GET /programs`, `POST /programs`, `PUT /programs/{id}`, `DELETE /programs/{id}`
 - [X] T031 [US3] 在 `backend/tests/test_contacts_programs.py` 新增 CRUD 測試，驗證新增後在 `GET /programs` 可見、在建立 release 時可選擇
 - [X] T032 [US3] 在 `backend/schemas.py` 補實作 `ContactSchema` 與 `ProgramSchema` 驗證規則（email 格式驗證）
 - [X] T033 [US3] 在 `backend/main.py` 註冊 `contacts.py` 與 `programs.py` 路由
 - [X] T034 [US3] [P] 新增管理 UI/示範請求片段於 `specs/001-release-announcements/quickstart.md`

---

## Phase 6: User Story 4 - 檢視發送紀錄與稽核 (Priority: P1)

Goal: 系統管理者可查詢每次發送紀錄並查看錯誤摘要以利稽核。

Independent Test: 使用 `GET /send_logs` 與過濾參數能回傳對應紀錄，失敗紀錄包含 detail 欄位。

- [ ] T035 [P] [US4] 在 `backend/api/send_logs.py`（建立新檔）實作 `GET /send_logs`（支援時間篩選、program 篩選）
- [ ] T036 [US4] 在 `backend/models.py` 確認 `SendLog` 模型並為 `SendLog` 加入索引以便查詢效率
- [ ] T037 [US4] 在 `backend/tests/test_send_logs.py` 實作查詢與過濾測試
- [ ] T038 [US4] 在 `specs/001-release-announcements/quickstart.md` 加入查詢 send_logs 的示例
- [ ] T039 [US4] 在 `backend/main.py` 註冊 `send_logs.py` 路由
 - [X] T035 [P] [US4] 在 `backend/api/send_logs.py`（建立新檔）實作 `GET /send_logs`（支援時間篩選、program 篩選）
 - [X] T036 [US4] 在 `backend/models.py` 確認 `SendLog` 模型並為 `SendLog` 加入索引以便查詢效率
 - [X] T037 [US4] 在 `backend/tests/test_send_logs.py` 實作查詢與過濾測試
 - [X] T038 [US4] 在 `specs/001-release-announcements/quickstart.md` 加入查詢 send_logs 的示例
 - [X] T039 [US4] 在 `backend/main.py` 註冊 `send_logs.py` 路由

---

## Phase 7: User Story 5 - 開發環境模擬與測試 (Priority: P2)

Goal: 在開發/測試環境模擬 SMTP 與失敗情境，確保 send_logs 能記錄失敗細節。

Independent Test: 在測試中模擬 SMTP 失敗，驗證 `SendLog` 包含 error detail 且 API 回傳預期狀態碼。

- [ ] T040 [P] [US5] 在 `backend/tests/conftest.py` 新增 SMTP 模擬 fixture（或使用第三方本機 smtp 模擬服務設定指引）
- [ ] T041 [US5] 在 `backend/tests/test_send_simulation.py` 實作模擬失敗測試（SMTP 連線失敗、逾時、單位收件失敗）
- [ ] T042 [US5] 在 `specs/001-release-announcements/quickstart.md` 新增如何在本機模擬 SMTP（MailHog / smtpd 範例）
 - [X] T040 [P] [US5] 在 `backend/tests/conftest.py` 新增 SMTP 模擬 fixture（或使用第三方本機 smtp 模擬服務設定指引）
 - [X] T041 [US5] 在 `backend/tests/test_send_simulation.py` 實作模擬失敗測試（SMTP 連線失敗、逾時、單位收件失敗）
 - [X] T042 [US5] 在 `specs/001-release-announcements/quickstart.md` 新增如何在本機模擬 SMTP（MailHog / smtpd 範例）
- [X] T043 [US5] [P] 新增 CI 測試腳本樣板 `/.github/workflows/ci.yml`（含 pytest 基本步驟，視專案需求決定是否立即啟用）

- [ ] T048 [US5] E2E latency test — 建立簡單的端對端測試腳本測量從建立 Release 到發送完成的平均時間（範例資料與 repeat runs），以驗證 SC-001（平均 <= 3 分鐘）。
- [ ] T049 [US5] SendLog query perf test — 在測試資料庫建立至少 1000 筆 `SendLog` 範例資料，驗證 `GET /send_logs` 在典型過濾條件下回應時間 < 2s，並在超過時產生優化紀錄。

---

## Final Phase: Polish & Cross-Cutting Concerns

- [X] T044 文件更新：更新 `specs/001-release-announcements/quickstart.md` 與 `README.md` 的運行指引
- [X] T045 安全性檢查：審查環境變數與日誌避免洩露敏感資訊（`backend/config.py`）
- [ ] T046 [P] 補充單元測試與整合測試，將測試覆蓋率提升至團隊同意的門檻（例如 70%）
- [ ] T047 代碼整理與 lint：在 `backend/` 執行格式化並修正警告（例如 use Black / ruff，視專案偏好）

- [X] T050 授權強制與測試：新增測試以驗證管理者/發佈者角色邊界（範例：非管理者呼叫 `POST /programs` 應回 403），並在 API 規格中列出需受保護的路由清單。
- [X] T051 Endpoint auth enforcement — 在 `backend/api/*` 主要路由（contacts/programs/releases/send/send_logs）明確註記必須驗證角色與返回 401/403 規範，並在 Acceptance Criteria 補充「未授權操作應返回 401/403」。

- [X] T052 Implement recipient count & validation checks — 在 `POST /releases/{id}/send` 實作收件人數量檢查（>500 回 400）與前置 email 格式驗證（無效 email 回 400），並加入對應單元測試。
- [X] T053 Error mapping & logging — 定義 API 與 `SendLog` 中常見錯誤的 code-mapping（例如 timeout->504, rate_limit->429, validation->400），並在 `backend/tests/` 新增對應的契約測試。
- [ ] T054 Update quickstart & docs — 在 `specs/001-release-announcements/quickstart.md` 加入使用者面對錯誤時的範例訊息與建議操作（如分批上傳、等待重試），並更新 quickstart 的 API 範例回應。

---

## 依賴關係（建議執行順序）

- Foundational (T006-T012) 必須先完成，才能開始任一 User Story 的實作。
- User Stories 以優先順序執行（US1, US2, US3, US4 為 P1；US5 為 P2），但在 Foundation 完成後可並行實作。

## 平行執行範例

- 可平行：`T008`（Schema 實作）、`T013`（Release model 實作）、`T021`（Recipient schema）等，因為檔案不同且互不阻塞。
- 建議分工：一位工程師完成 Foundation；其餘工程師分配至不同 User Story 的 models/services/endpoints。

## Implementation strategy

- MVP-first：優先完成 Phase 1 + Phase 2，接著實作 User Story 1，通過驗證後視情況發布最小可行功能。
- Incremental：每完成一個 User Story，立即執行獨立測試並更新 Quickstart 範例。

---

## 產出路徑與摘要

- 產出檔案：`specs/001-release-announcements/tasks.md`（本檔）

總任務數：47

任務數（按使用者故事）:
- US1: 8
- US2: 8
- US3: 6
- US4: 5
- US5: 4
- Setup/Foundational/Polish: 16

平行機會：多個 schema、model、tests 可同時實作（標註 [P]），建議在 Foundation 完成後分工並行開發。

建議 MVP 範圍：僅實作 Phase1 + Phase2 + User Story 1（T001-T020）。

格式驗證：所有任務均遵循 checklist 格式（- [ ] T### [P]? [US?]? 描述並包含檔案路徑）。
