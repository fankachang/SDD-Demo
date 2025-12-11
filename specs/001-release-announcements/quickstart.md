# Quickstart — 本地開發 (Python 3.14)

假設你使用 Python 3.14 的虛擬環境（`venv`），以下步驟可讓你在本機啟動 MVP 後端：

1. 建立並啟用虛擬環境（若尚未建立）

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

2. 安裝相依套件

```bash
pip install -r backend/requirements.txt
```

(`backend/requirements.txt` 包含：`fastapi`, `uvicorn[standard]`, `sqlalchemy`, `alembic`, `jinja2`, `email-validator`, `python-dotenv`, `pytest`)

3. 設定環境變數（範例）

```bash
export SMTP_HOST=smtp.example.com
export SMTP_PORT=587
export SMTP_USER=you@example.com
export SMTP_PASS=secret
export DATABASE_URL=sqlite:///./dev.db
```

4. 執行資料庫遷移（若使用 Alembic）

```bash
cd backend
alembic upgrade head
```

5. 啟動開發伺服器

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

6. 使用 OpenAPI 文件測試 API

開啟 `http://localhost:8000/docs`（由 FastAPI 自動產生）或使用 `specs/001-release-announcements/contracts/openapi.yaml` 作為合約參考。

7. 測試

```bash
pytest
```

備註：若你沒有可用的 SMTP 測試環境，可以使用本機模擬 SMTP（例如 `smtpd` 或 `mailhog`）以檢查郵件輸出，而不實際寄送到外部收件者。

## 錯誤回應與使用者處理建議（範例）

在開發或整合 API 時，請參考以下常見錯誤回應與建議處理方式，這些範例會幫助前端與測試人員在遇到錯誤時提供一致的使用者經驗：

- 400 Bad Request（驗證或參數錯誤）

	範例：當 `POST /releases/{id}/send` 傳入超過 500 位收件人或包含無效 email 時，API 應回 400 並回傳錯誤說明。

	範例回應：

	```json
	{
		"error": "validation_error",
		"details": {
			"recipients": "too_many_recipients > 500",
			"invalid_emails": ["bad-email@", "no-at-symbol"]
		}
	}
	```

	建議前端行為：顯示欄位錯誤訊息，並提示使用者分批上傳或修正錯誤的電子郵件格式。

- 504 Gateway Timeout（SMTP 同步發送逾時）

	範例回應：

	```json
	{ "error": "timeout", "message": "SMTP request timed out (30s)" }
	```

	建議前端行為：顯示超時訊息，並讓使用者選擇稍後重試或改用小量分批發送；同時在 UI 中提供發送紀錄連結以便查看失敗明細。

- 429 / 503（速率或服務不可用）

	範例回應：

	```json
	{ "error": "rate_limit", "message": "SMTP provider rate limit, try again later" }
	```

	建議前端行為：提示使用者稍後再試，或提供分批發送的建議與說明。

## 範例 curl：發送 release（含 error handling 範例）

範例（成功或部分失敗時，API 回傳 `SendLog`）：

```bash
curl -X POST "http://localhost:8000/releases/1/send" \
	-H "Content-Type: application/json" \
	-d '{"recipients": [{"email":"alice@example.com","type":"to"},{"email":"bob@example.com","type":"bcc"}]}'
```

若回傳 400/504/429，請依上方建議在 UI 顯示相對處理步驟。

## 查詢發送紀錄（Send Logs）範例

系統支援透過 `GET /send_logs` 查詢發送紀錄，並可使用參數過濾：

- `program_id`：依程式（Program）篩選
- `start` / `end`：時間區間（ISO 8601 格式）
- `result`：發送結果（`success`、`failure`、`timeout`）
- `page` / `page_size`：分頁

範例：查詢某程式在時間區間內的成功發送紀錄（第一頁，最多 10 筆）

```bash
curl -X GET "http://localhost:8000/send_logs?program_id=5&start=2025-01-01T00:00:00Z&end=2025-12-31T23:59:59Z&result=success&page=1&page_size=10"
```

回應範例（200）：

```json
[
	{
		"id": 123,
		"release_id": 45,
		"sent_at": "2025-06-01T12:34:56",
		"result": "success",
		"detail": "sent to 3 recipients"
	}
]
```

建議：將此 API 用於後台稽核頁面，並在 UI 提供導出或按條件篩選的功能以利調查失敗紀錄。

## 本機模擬 SMTP（開發 / 測試）

在本地測試時，建議使用模擬 SMTP 以避免將測試郵件送到外部收件者。以下為常見做法：

- 使用 MailHog（推薦）：透過 Docker 快速啟動一個抓取郵件的介面。

```bash
# 使用 Docker 啟動 MailHog（在本機 http://localhost:8025 檢視郵件）
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog

# 將環境變數指向本機 MailHog
export SMTP_HOST=localhost
export SMTP_PORT=1025
```

- 使用 Mailpit（替代方案）：

```bash
docker run -p 1025:1025 -p 8025:8025 axllent/mailpit
export SMTP_HOST=localhost
export SMTP_PORT=1025
```

- 簡易 Python 模擬（不需 Docker）：使用標準庫的簡易 debug server（僅供開發使用）：

```bash
# 在一個終端執行
python -m smtpd -n -c DebuggingServer localhost:1025

# 在另一個終端設環境變數並啟動應用程式
export SMTP_HOST=localhost
export SMTP_PORT=1025
```

注意：上述方式僅供開發/測試環境，生產環境請使用正式 SMTP 提供者並妥善設定認證與 TLS。若使用模擬服務，記得在 CI 或測試腳本中指向模擬主機或使用相應的測試 fixture。