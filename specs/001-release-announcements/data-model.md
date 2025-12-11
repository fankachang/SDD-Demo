# Data Model — 程式版本發佈 (Release Announcements)

以下資料模型根據 `spec.md` 要求設計，欄位以最小必要性為主，並包含驗證規則與關聯性。

## Entities

- User
  - id: integer (PK)
  - email: string (unique, required, email格式)
  - name: string (required)
  - role: enum [admin, publisher] (required)
  - password_hash: string (required)
  - created_at: datetime
  - updated_at: datetime

- Program
  - id: integer (PK)
  - name: string (required)
  - description: text (optional)
  - created_at: datetime
  - updated_at: datetime

- Contact
  - id: integer (PK)
  - name: string (required)
  - email: string (required, email格式)
  - group: string (nullable)
  - created_by: integer (FK -> User.id)
  - created_at: datetime
  - updated_at: datetime

- Release
  - id: integer (PK)
  - program_id: integer (FK -> Program.id, required)
  - version: string (required)
  - notes: text (optional)
  - created_by: integer (FK -> User.id)
  - status: enum [draft, previewed, sent]
  - created_at: datetime
  - updated_at: datetime

- ReleaseRecipient (recipient snapshot)
  - id: integer (PK)
  - release_id: integer (FK -> Release.id)
  - contact_id: integer (nullable, FK -> Contact.id)
  - email: string (required)
  - recipient_type: enum [to, cc, bcc]

- SendLog
  - id: integer (PK)
  - release_id: integer (FK -> Release.id)
  - sent_at: datetime
  - result: enum [success, failure, timeout]
  - detail: text (錯誤或外部回應摘要)

## 關聯性

- `User` (1) — (M) `Release` via `created_by`。
- `Program` (1) — (M) `Release`。
- `Release` (1) — (M) `ReleaseRecipient`。
- `Release` (1) — (M) `SendLog`（每次發送會產生一筆 SendLog）。

## 驗證規則

- email 欄位使用嚴格電子郵件格式驗證。
- Release 在從 `draft` 轉為 `previewed` 前，必須有 `program_id`、`version` 與至少一位 recipient。
- 同步發送 API 在接受請求時，若 recipients 數量 > 500 則拒絕並回傳 400 錯誤。
- 同步發送在 API 層僅做單次 SMTP 嘗試（不自動重試）；若逾時或失敗，結果在 `SendLog` 中記錄詳細資訊。

## State transitions (Release)

- draft -> previewed : 當使用者在 UI 完成 Step1, 驗證通過並點選下一步
- previewed -> sent : 使用者在 Step3 點擊「發送」，系統執行同步 SMTP 嘗試並建立 `SendLog`，若 API 成功回傳則狀態為 `sent`，否則仍記錄失敗於 `SendLog` 並可依需要由背景工作排隊重試（非同步機制為未來擴充）

