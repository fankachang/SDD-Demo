# 開發者 Quickstart

本檔為專案快速啟動與測試指引（給開發者）

快速在本機啟動後端與測試（假設已建立並啟用虛擬環境 `.venv`）：

```bash
# 建立虛擬環境（若尚未建立）
python3.14 -m venv .venv
source .venv/bin/activate

# 安裝相依
pip install -r backend/requirements.txt

# 設定環境變數範例（開發用）
export DATABASE_URL=sqlite:///./dev.db
export SMTP_HOST=localhost
export SMTP_PORT=1025

# 執行資料庫（若使用 Alembic）或直接建立表格
# cd backend && alembic upgrade head

# 啟動開發伺服器
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 或在另一個終端執行測試
pytest
```

更多細節請參閱 `specs/001-release-announcements/quickstart.md`（包含 `send_logs` 與本機 SMTP 模擬說明）。

PR 與狀態：目前變更已開 PR，參考：https://github.com/fankachang/SDD-Demo/pull/3
