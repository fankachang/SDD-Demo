"""錯誤碼定義與映射 - 統一 API 和 SendLog 的錯誤處理

本模組定義了系統中常見錯誤的標準碼與訊息，確保前端能一致處理錯誤狀況。
"""

from enum import Enum
from typing import Dict, Optional


class ErrorCode(str, Enum):
    """標準錯誤碼"""

    # 驗證錯誤 (400)
    VALIDATION_ERROR = "validation_error"
    TOO_MANY_RECIPIENTS = "too_many_recipients"
    INVALID_EMAIL = "invalid_email"
    MISSING_REQUIRED_FIELD = "missing_required_field"

    # 授權錯誤 (401, 403)
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"

    # 資源錯誤 (404)
    NOT_FOUND = "not_found"
    RELEASE_NOT_FOUND = "release_not_found"
    PROGRAM_NOT_FOUND = "program_not_found"
    CONTACT_NOT_FOUND = "contact_not_found"

    # SMTP 相關錯誤
    SMTP_CONNECTION_ERROR = "smtp_connection_error"
    SMTP_AUTH_ERROR = "smtp_auth_error"
    SMTP_TIMEOUT = "smtp_timeout"
    SMTP_SEND_ERROR = "smtp_send_error"

    # 速率限制 (429)
    RATE_LIMIT = "rate_limit"

    # 超時 (504)
    TIMEOUT = "timeout"
    GATEWAY_TIMEOUT = "gateway_timeout"

    # 伺服器錯誤 (500)
    INTERNAL_ERROR = "internal_error"
    DATABASE_ERROR = "database_error"
    SERVICE_UNAVAILABLE = "service_unavailable"


class SendLogResult(str, Enum):
    """SendLog 結果狀態"""

    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    PARTIAL = "partial"  # 部分成功部分失敗


# HTTP 狀態碼對應
ERROR_CODE_TO_HTTP_STATUS: Dict[ErrorCode, int] = {
    # 400 系列
    ErrorCode.VALIDATION_ERROR: 400,
    ErrorCode.TOO_MANY_RECIPIENTS: 400,
    ErrorCode.INVALID_EMAIL: 400,
    ErrorCode.MISSING_REQUIRED_FIELD: 400,
    # 401
    ErrorCode.UNAUTHORIZED: 401,
    ErrorCode.INVALID_TOKEN: 401,
    ErrorCode.EXPIRED_TOKEN: 401,
    # 403
    ErrorCode.FORBIDDEN: 403,
    # 404
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.RELEASE_NOT_FOUND: 404,
    ErrorCode.PROGRAM_NOT_FOUND: 404,
    ErrorCode.CONTACT_NOT_FOUND: 404,
    # 429
    ErrorCode.RATE_LIMIT: 429,
    # 500 系列
    ErrorCode.INTERNAL_ERROR: 500,
    ErrorCode.DATABASE_ERROR: 500,
    ErrorCode.SMTP_CONNECTION_ERROR: 500,
    ErrorCode.SMTP_AUTH_ERROR: 500,
    ErrorCode.SMTP_SEND_ERROR: 500,
    # 503
    ErrorCode.SERVICE_UNAVAILABLE: 503,
    # 504
    ErrorCode.TIMEOUT: 504,
    ErrorCode.GATEWAY_TIMEOUT: 504,
    ErrorCode.SMTP_TIMEOUT: 504,
}


# 使用者友善的錯誤訊息（繁體中文）
ERROR_MESSAGES_ZH_TW: Dict[ErrorCode, str] = {
    # 驗證錯誤
    ErrorCode.VALIDATION_ERROR: "資料驗證失敗",
    ErrorCode.TOO_MANY_RECIPIENTS: "收件人數量超過限制（最多 500 位）",
    ErrorCode.INVALID_EMAIL: "電子郵件格式不正確",
    ErrorCode.MISSING_REQUIRED_FIELD: "缺少必要欄位",
    # 授權錯誤
    ErrorCode.UNAUTHORIZED: "未授權，請先登入",
    ErrorCode.FORBIDDEN: "權限不足，無法執行此操作",
    ErrorCode.INVALID_TOKEN: "登入憑證無效",
    ErrorCode.EXPIRED_TOKEN: "登入憑證已過期，請重新登入",
    # 資源錯誤
    ErrorCode.NOT_FOUND: "找不到指定的資源",
    ErrorCode.RELEASE_NOT_FOUND: "找不到指定的發佈記錄",
    ErrorCode.PROGRAM_NOT_FOUND: "找不到指定的程式",
    ErrorCode.CONTACT_NOT_FOUND: "找不到指定的聯絡人",
    # SMTP 錯誤
    ErrorCode.SMTP_CONNECTION_ERROR: "無法連線到郵件伺服器",
    ErrorCode.SMTP_AUTH_ERROR: "郵件伺服器認證失敗",
    ErrorCode.SMTP_TIMEOUT: "郵件發送超時（30 秒）",
    ErrorCode.SMTP_SEND_ERROR: "郵件發送失敗",
    # 速率限制
    ErrorCode.RATE_LIMIT: "請求過於頻繁，請稍後再試",
    # 超時
    ErrorCode.TIMEOUT: "操作超時，請稍後再試",
    ErrorCode.GATEWAY_TIMEOUT: "閘道超時",
    # 伺服器錯誤
    ErrorCode.INTERNAL_ERROR: "伺服器內部錯誤",
    ErrorCode.DATABASE_ERROR: "資料庫錯誤",
    ErrorCode.SERVICE_UNAVAILABLE: "服務暫時無法使用",
}


# 使用者建議操作
ERROR_SUGGESTIONS_ZH_TW: Dict[ErrorCode, str] = {
    ErrorCode.TOO_MANY_RECIPIENTS: "請將收件人分批處理，每批最多 500 位",
    ErrorCode.INVALID_EMAIL: "請檢查並修正無效的電子郵件地址",
    ErrorCode.UNAUTHORIZED: "請返回登入頁面重新登入",
    ErrorCode.EXPIRED_TOKEN: "請重新登入以繼續操作",
    ErrorCode.FORBIDDEN: "請聯絡管理員申請適當的權限",
    ErrorCode.SMTP_TIMEOUT: "郵件伺服器回應緩慢，建議稍後重試或減少收件人數量",
    ErrorCode.SMTP_CONNECTION_ERROR: "請檢查網路連線或聯絡系統管理員",
    ErrorCode.RATE_LIMIT: "您的操作過於頻繁，請等待片刻後再試",
    ErrorCode.SERVICE_UNAVAILABLE: "服務正在維護中，請稍後再試",
}


def create_error_response(
    error_code: ErrorCode,
    details: Optional[Dict] = None,
    custom_message: Optional[str] = None,
) -> Dict:
    """
    建立標準錯誤回應

    Args:
        error_code: 錯誤碼
        details: 額外的錯誤詳情
        custom_message: 自訂訊息（覆蓋預設訊息）

    Returns:
        標準化的錯誤回應字典
    """
    response = {
        "error": error_code.value,
        "message": custom_message or ERROR_MESSAGES_ZH_TW.get(error_code, "未知錯誤"),
    }

    if details:
        response["details"] = details

    # 加入建議操作（如果有）
    suggestion = ERROR_SUGGESTIONS_ZH_TW.get(error_code)
    if suggestion:
        response["suggestion"] = suggestion

    return response


def map_exception_to_error_code(exception: Exception) -> ErrorCode:
    """
    將 Python 例外映射到標準錯誤碼

    Args:
        exception: Python 例外物件

    Returns:
        對應的錯誤碼
    """
    exception_name = type(exception).__name__

    # 常見例外映射
    mapping = {
        "TimeoutError": ErrorCode.TIMEOUT,
        "ValueError": ErrorCode.VALIDATION_ERROR,
        "KeyError": ErrorCode.NOT_FOUND,
        "PermissionError": ErrorCode.FORBIDDEN,
        "ConnectionError": ErrorCode.SMTP_CONNECTION_ERROR,
        "SMTPAuthenticationError": ErrorCode.SMTP_AUTH_ERROR,
        "SMTPException": ErrorCode.SMTP_SEND_ERROR,
    }

    return mapping.get(exception_name, ErrorCode.INTERNAL_ERROR)


def create_sendlog_detail(
    result: SendLogResult,
    error_code: Optional[ErrorCode] = None,
    smtp_response: Optional[str] = None,
    recipient_results: Optional[list] = None,
) -> Dict:
    """
    建立 SendLog 的 detail 欄位

    Args:
        result: 發送結果
        error_code: 錯誤碼（如果失敗）
        smtp_response: SMTP 伺服器回應
        recipient_results: 個別收件人結果清單

    Returns:
        SendLog detail 字典
    """
    detail = {
        "code": error_code.value if error_code else "OK",
        "message": (
            ERROR_MESSAGES_ZH_TW.get(error_code, "發送成功")
            if error_code
            else "發送成功"
        ),
    }

    if smtp_response:
        detail["smtp_response"] = smtp_response

    if recipient_results:
        detail["recipient_results"] = recipient_results

    return detail
