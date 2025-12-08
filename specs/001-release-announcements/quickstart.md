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