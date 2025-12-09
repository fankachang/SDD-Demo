# Feature Specification: 程式版本發佈網站（Release Announcements）

注意：除憲章外，使用者面向的規格與說明文件均以繁體中文（zh-TW）撰寫。

**Feature Branch**: `001-release-announcements`  
**Created**: 2025-12-07  
**Status**: Draft  
**Input**: User description: "程式版本發佈網站 — 建立發佈三步驟流程、郵件寄送、收件人與程式管理（MVP）"

## Clarifications

### Session 2025-12-07

- Q: 認證方式應採何種方式？ → A: 使用簡易 email/password 登入並以伺服器端 Session 管理（短期方案，未來可升級為 JWT/SSO）。
- Q: 發送方式要採同步或非同步？ → A: 同步直接發送（透過 SMTP），API 呼叫會等候 SMTP 回應並回傳成功或失敗。
- Q: 單次發佈預期最大收件人量為多少？ → A: 單次上限設為 <= 500 收件人（若超過需採分批或升級為非同步架構）。
- Q: 同步發送時是否執行自動重試或重發機制？ → A: 否，採單次 SMTP 嘗試；系統預期使用者管理之收件地址均為有效，系統不做自動重試或回滾，僅記錄每位收件人的結果。
- Q: 同步發送 API 最長等待 SMTP 回應的 timeout 要多少？ → A: API 同步發送 timeout 設為 30 秒（短期上限，避免長時間阻塞）。
- Q: 是否在 MVP 驗證 "成功送達率 >= 98%"（SC-002）？ → A: 否。由使用者管理收件對象，MVP 不需驗證發送成功率或模擬失敗率。

### Session 2025-12-08

- Q: 發送失敗時的重發/重試策略應採何種方式？ → A: 採伺服器端背景工作（排入佇列，由後端非同步處理），同步 API 仍維持單次 SMTP 嘗試並即時回傳結果。

註：伺服器端背景重試（background retry）為未來擴充，非本次 MVP 必須實作。MVP 要求：同步 API 僅執行單次 SMTP 嘗試並回傳結果；對失敗的嘗試需產生可查詢的 `SendLog` 紀錄，以便未來背景工作或人工介入處理。若要在本次開發中實作背景重試，請將該工作列為後續迭代任務並取得專案核准。

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - 建立發佈草稿與預覽 (Priority: P1)

作為發佈者，我要在發佈表單輸入程式名稱、版本與配合事項並進入預覽，讓我能在發送前確認內容。

**Why this priority**: 這是核心流程的第一步，完成後可確保內容正確再發送，對使用者價值最高。

**Independent Test**: 在發佈介面輸入必要欄位並按下一步，可看到包含標題、內容、收件人預覽的完整預覽畫面。

**Acceptance Scenarios**:

1. **Given** 使用者在系統已登入且有發佈權限，**When** 在發佈表單填寫程式名稱、版本與內容並按「下一步」，**Then** 顯示郵件標題與內文的預覽畫面，且禁止缺少必填欄位時進入預覽。
2. **Given** 使用者在預覽畫面發現錯誤，**When** 點選「返回編輯」，**Then** 返回步驟1並保留先前輸入的資料。

---

### User Story 2 - 選擇收件人並發送 (Priority: P1)

作為發佈者，我可以在步驟三選擇收件人（To/CC/BCC）並執行發送，確保指定對象收到郵件。

**Why this priority**: 發送動作是系統核心功能，沒有發送功能則無法完成任務。

**Independent Test**: 在預覽畫面點選收件人清單，執行發送後能收到即時狀態反饋且發送紀錄被建立。

**Acceptance Scenarios**:

1. **Given** 已完成預覽並選取收件人，**When** 點擊「發送」，**Then** 系統顯示發送進度、最終結果（成功/失敗）並儲存發送紀錄。
2. **Given** 選取 BCC 的收件人，**When** 郵件送達，**Then** BCC 收件人不會出現在其他收件者的 To/CC 名單中。

---

### User Story 3 - 收件人與程式清單管理 (Priority: P1)

作為管理者，我要能新增/編輯/刪除收件人（含姓名、電子郵件、群組）以及管理可發佈程式列表，確保發佈者可從清單中選擇正確程式。

**Why this priority**: 管理介面讓使用者資料與程式列表一致且可維護，是系統能正確發送的前提。

**Independent Test**: 透過管理介面執行新增、編輯、刪除操作，變更應即時反映在發佈表單的下拉選單與收件人清單。

**Acceptance Scenarios**:

1. **Given** 管理者登入，**When** 新增或更新收件人資料，**Then** 該收件人在發佈選單中可被選取。
2. **Given** 管理者刪除某程式，**When** 發佈者開啟表單，**Then** 該程式不會出現在下拉選單中。

---

### User Story 4 - 檢視發送紀錄與稽核 (Priority: P1)

作為系統管理者，我能查詢每次發送的紀錄（時間、發佈者、程式名稱、版本、收件人、結果與錯誤訊息），以利稽核與問題調查。

**Why this priority**: 發送紀錄是稽核與錯誤追蹤的必要資料。

**Independent Test**: 在紀錄查詢頁面搜索並過濾結果能返回符合條件的發送紀錄；失敗紀錄顯示錯誤原因。

**Acceptance Scenarios**:

1. **Given** 系統記錄多次發送，**When** 管理者使用時間範圍或程式名稱過濾，**Then** 列表僅顯示符合條件的結果。
2. **Given** 某次發送失敗，**When** 檢視詳細紀錄，**Then** 可見失敗原因與系統回應摘要。

### User Story 5 - 開發環境模擬與測試 (Priority: P2)

作為測試人員，我要能在開發環境模擬發送並檢查失敗時的錯誤訊息與重試機制，確保系統在真實錯誤條件下有可觀察的行為與紀錄。

**Why this priority**: 測試可確保發送流程健壯並在錯誤時能回溯資料。

**Independent Test**: 在測試環境模擬郵件發送失敗，檢查系統是否記錄錯誤並在日誌/紀錄中保存失敗細節。

**Acceptance Scenarios**:

1. **Given** 測試環境中故意模擬郵件傳送錯誤，**When** 發送嘗試完成，**Then** send_logs 顯示失敗且 detail 欄位包含錯誤摘要。

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

-- 當發送服務臨時不可用時，系統應將發送標記為失敗並保留可查詢的錯誤原因與原始收件人快照。
-- 當收件人電子郵件格式無效或收件伺服器拒收時，系統應在發送結果中儲存錯誤原因並標註該收件地址為失敗。
-- 當大量收件人造成發送併發或速率限制，被郵件服務拒絕時，系統應提供分批或重試策略的設計備註以便未來實作（此為 P1 範圍內非即時需求）。
-- 若系統採用同步直接發送且單次收件人數 > 500，系統應阻止該同步操作並提示使用者分批發送或切換至非同步處理策略以避免超時或失敗。

-- 系統將提供後端非同步重試（background retry）機制：對於發送失敗的紀錄，可排入後端重試佇列由背景工作處理；此機制不會改變同步 API 的單次嘗試限制，且重試次數/間隔等策略將在 implementation 階段定義。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: 系統 MUST 提供發佈三步驟流程：建立發佈 (程式、版本、說明) → 預覽 (郵件標題/內文/收件人預覽) → 發送（含即時狀態回饋）。
- **FR-002**: 系統 MUST 支援選取收件人並區分 To/CC/BCC，並在發送時將當時的收件人快照儲存於發送紀錄中。
- **FR-003**: 系統 MUST 提供收件人管理（CRUD），欄位包含：姓名、電子郵件、所屬群組（可選）、建立者與時間戳記。
- **FR-004**: 系統 MUST 提供可發佈程式清單（CRUD），供發佈表單的下拉選擇使用。
- **FR-005**: 系統 MUST 在每次發送完成後產生發送紀錄（send_logs），記錄：時間、發佈者、程式名稱、版本、收件人快照、結果（成功/失敗）與錯誤說明（若有）。
- **FR-006**: 系統 MUST 在發佈流程中做基本驗證：必填欄位檢查、有效郵件格式驗證、並在驗證失敗時阻止進行下一步。
- **FR-007**: 系統 MUST 支援在開發/測試環境模擬失敗並將錯誤細節記錄於 send_logs（便於測試與重試流程驗證）。
 
 - **FR-008**: 系統 MUST 有最小授權機制，初期採用簡易 email/password 登入與伺服器端 session 管理；僅授權角色（管理者/發佈者）可進行對應的管理或發佈操作，且操作需記錄操作者資訊於發送紀錄。
 - **FR-009**: 系統 MUST 支援同步直接透過 SMTP 進行發送；當使用同步模式時，系統應限制單次發送之收件人數量上限為 500 人，超過時需阻止同步發送並提示分批或改用非同步佇列策略。
 - **FR-010**: 系統 MUST 在同步發送情境下僅執行單次 SMTP 嘗試（不作自動重試）；系統需對每個收件人記錄成功或失敗結果並儲存在 send_logs 中；若個別收件失敗，應記錄失敗原因但不回滾已送達的收件。
 - **FR-011**: 系統 MUST 為同步發送設定 API timeout（上限 30 秒）；當 timeout 發生時，API 應回傳 timeout 錯誤並在 send_logs 記錄相關超時資訊與受影響收件人（如有）。

### Key Entities

- **User**：系統使用者，主要屬性：id、email、name、role（管理者/發佈者）、created_at/updated_at。
- **Program（可發佈程式）**：可發佈的程式項目，主要屬性：id、name、description、created_at/updated_at。
- **Contact（收件人）**：收件人資料，主要屬性：id、name、email、group_id（nullable）、created_by、created_at/updated_at。
- **Release（發佈草稿/紀錄）**：發佈內容，主要屬性：id、program_id、version、notes、created_by、status（draft/previewed/sent）、created_at/updated_at。
- **ReleaseRecipient（發佈收件人快照）**：每次發佈的收件人快照，主要屬性：id、release_id、contact_id (nullable)、email、recipient_type（to/cc/bcc）。
- **SendLog（發送日誌）**：發送結果記錄，主要屬性：id、release_id、sent_at、result（success/failure）、detail（錯誤或外部回應摘要）。

  - **SendLog.detail 範例結構（JSON schema 簡述）**：為了讓前後端與測試擁有一致的解析格式，建議 detail 欄位採用下列結構（JSON object）：
    {
      "code": "string (optional, machine-readable error code)",
      "message": "string (human-readable summary)",
      "smtp_response": "string (原始 SMTP 回應或摘要, optional)",
      "recipient_results": [
        {"email":"string","status":"success|failure","code":"string?","message":"string?"}
      ]
    }
  
  實作時可在資料庫以 JSON/text 儲存該結構，並於 contracts/openapi.yaml 中定義 `SendLogDetail` schema 以作為 API response 的共同契約。

## Success Criteria (必備)

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### 可測量成功指標

- **SC-001**：使用者能在三個步驟內完成一次發佈（建立 → 預覽 → 發送），從開始填表到發送完成平均時間不超過 3 分鐘（測試場景可重現）。
 - **SC-002**：此 MVP 不將「成功送達率」作為驗收準則；發送/失敗分析屬於未來擴充或測試項，收件人清單管理留給使用者負責（不在 MVP 中驗證發信失敗）。
- **SC-003**：系統能列出並搜尋歷史發送紀錄，查詢回應時間於常規資料量下 < 2 秒（可透過範例資料驗證）。
- **SC-004**：收件人管理與程式清單 CRUD 操作能在執行後即時反映於發佈表單下拉與選單（驗證透過 UI 操作與資料一致性檢查）。

### 附加成功驗收條件

- 發送失敗的紀錄包含可讀錯誤摘要（detail）以利稽核與後續處理。
- BCC 收件人不會在其他收件者的 To/CC 清單中顯示。

## 範圍（Scope）

- 本規格屬於 MVP（P0）範疇，包含：發佈三步驟流程、郵件寄送、收件人管理、程式清單管理、發送紀錄查詢與基本授權機制。
- 不在本次 MVP 範圍內（P1 / P2 可列為後續）：群組規則進階邏輯、CSV 批次匯入、進階權限管理介面、多語系支援、Webhook 或其他外部通知渠道（如 SMS/Slack）。

## 依賴與假設

- 假設系統在部署/測試環境可接入一個郵件投遞途徑（或模擬投遞），以驗證發送流程。
- 假設初期使用輕量資料庫（例如 SQLite）以便開發與測試，資料模型與遷移策略需支援未來遷移到其他關聯式資料庫。
- 假設敏感資料（例如郵件認證）會以環境變數或安全方式存放與管理，規格中不包含憑證管理細節。

## Acceptance Criteria — FR -> 可驗證項目

- **FR-001**（發佈三步驟流程）:
  - 發佈者能在 UI 上依序完成 Step1 → Step2 → Step3，Step2 有完整的預覽，Step3 可發送，且流程中的必填驗證會阻止非完整資料的流轉。

- **FR-002**（To/CC/BCC 與收件人快照）:
  - 發送時收件人列表可區分 To、CC、BCC；發送記錄中保存當時的每位收件人與其類型；模擬發送檢查 BCC 不出現在他人清單。

- **FR-003**（收件人管理 CRUD）:
  - 管理者可新增/編輯/刪除收件人；操作後發佈表單能立即反映變更；新增的無效電子郵件會被拒絕。

- **FR-004**（程式清單 CRUD）:
  - 管理者可新增/編輯/刪除程式；發佈者在建立發佈時從下拉中選擇；刪除項目不再出現在發佈下拉中。

- **FR-005**（發送紀錄）:
  - 每次發送後在 send_logs 產生一筆紀錄，包含時間、發佈者、程式、版本、收件人快照、結果與錯誤摘要（如適用）。

- **FR-006**（驗證）:
  - 必填欄位未完整或電子郵件格式錯誤時，無法進入預覽或發送，並顯示明確的錯誤訊息。

- **FR-007**（測試環境模擬）:
  - 在測試環境能模擬發送失敗，並在 send_logs 中查看 detail 欄位包含錯誤摘要。

- **FR-008**（授權機制）:
  - 系統僅允許具備授權角色的使用者執行管理或發佈操作；發送紀錄需記錄操作者身份。

- **FR-009**（同步發送與規模）:
   - **FR-010**（單次嘗試與紀錄）:
    - **FR-011**（API Timeout）:
      - 當系統在同步發送時，API 的同步呼叫等待 SMTP 的最大容忍時間為 30 秒；若超過 30 秒，API 應回傳 timeout 錯誤並在 send_logs 中標記該發送嘗試為超時與受影響收件人（可用概要訊息）。
    - 在同步發送流程中，系統應對每位收件人執行單次 SMTP 嘗試並在 send_logs 中記錄每位收件人的結果與錯誤摘要；系統不應在 API 層自動重試或整體回滾。
  - 當系統採用同步 SMTP 發送時，API 必須等待 SMTP 回應並回傳成功/失敗；對單次收件人數 <= 500 的發送，系統應允許同步發送並記錄結果；對超過 500 人的請求，系統應阻止同步發送並提示分批或改用非同步處理。

## 附註

- 實作時，技術決策（例如郵件傳遞方式、同步/非同步發送、重試實作）會在 implementation 階段明確定義，並依需求進行擴充。
 - 建議：系統應在 implementation 階段納入後端非同步重試機制（background retry queue），以便非同步重試先前記錄為失敗的發送；此建議不改變同步 API 的單次嘗試原則，具體重試策略將另行定義。

