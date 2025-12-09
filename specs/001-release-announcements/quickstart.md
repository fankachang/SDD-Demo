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