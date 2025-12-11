## 安全審查摘要（T045）

更新日期：2025-12-09

概述：本次針對環境變數管理與日誌可能洩露敏感資訊之風險執行最小可行修改（Minimal, safe changes）。

已完成項目：
- 新增 `backend/config.py`：集中讀取環境變數（`Config`），並提供 `redact_mapping` 與 `SecretFilter` 以遮蔽/過濾日誌中出現的敏感值。 
- 在 `backend/main.py` 的啟動流程附加 `SecretFilter` 至 root logger，並記錄「遮蔽後」的設定摘要以供除錯。
- 在 `backend/services/mailer.py` 使用 `get_logger()` 並加入送信前 / 例外時之記錄（logger.exception），以利稽核但避免直接暴露秘密。
- 將 `backend/emailer.py` 改為使用 `backend.config.cfg` 中的集中設定，避免直接於模組中散佈 `os.getenv` 呼叫。
- 新增測試 `backend/tests/test_config.py`：驗證 `redact_mapping` 與 `SecretFilter` 會遮蔽敏感值。

測試狀態：
- 本地測試執行結果：`10 passed, 42 warnings`（包含新增的 config redaction 測試）。

提交與分支：
- 變更已 commit 並推送至分支 `001-release-announcements`（包含 `backend/config.py`、logger 連接、測試與 `emailer` 的改寫）。

後續建議（非阻斷）：
1. 在 CI workflow 中加入一次性 secret-redaction smoke test（在乾淨環境下設置假的 secret，檢查日誌輸出不含原始 secret）。
2. 將其他模組（若有）逐步改為從 `backend.config.cfg` 取用設定，並移除散佈的 `os.getenv` 呼叫以集中管理。
3. 若要更嚴格：引入 `python-dotenv` 或 secrets manager（HashiCorp/Cloud KMS）並在部署流程中建立 secret 注入策略。

結語：已完成最小變更以降低敏感資訊在日誌中被曝光的風險，並補上測試以驗證遮蔽效果。建議下一步為將此安全摘要加入 PR 描述供 reviewers 參考，並在 CI 中加入自動驗證步驟。
