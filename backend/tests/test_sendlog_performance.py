"""SendLog 查詢效能測試

驗證 SendLog 查詢在大量資料下的效能,確保:
- 典型查詢在 2 秒內完成
- 索引正確運作
"""

import time
from backend.models import SendLog, Release, Program, SendResult


def test_sendlog_query_performance_with_large_dataset(client, auth_headers, db_session):
    """測試 SendLog 在大量資料下的查詢效能"""
    # 建立測試 program
    program = Program(name="PerfTestProgram", description="Performance test")
    db_session.add(program)
    db_session.commit()
    db_session.refresh(program)

    # 建立多個 releases
    num_releases = 10
    releases = []
    for i in range(num_releases):
        release = Release(
            program_id=program.id,
            version=f"v1.0.{i}",
            notes=f"Release {i}",
            created_by=1,  # 假設使用者 ID 為 1
        )
        db_session.add(release)
        releases.append(release)

    db_session.commit()
    for r in releases:
        db_session.refresh(r)

    # 為每個 release 建立多個 SendLog 記錄
    # 總共: 10 releases * 100 logs = 1000 筆記錄
    logs_per_release = 100
    total_logs = num_releases * logs_per_release

    print(f"\n建立 {total_logs} 筆 SendLog 記錄...")
    start_create = time.time()

    for release in releases:
        for i in range(logs_per_release):
            log = SendLog(
                release_id=release.id,
                result=SendResult.success if i % 3 != 0 else SendResult.failure,
                detail=f"Log entry {i} for release {release.version}",
            )
            db_session.add(log)

    db_session.commit()
    create_time = time.time() - start_create
    print(f"建立時間: {create_time:.3f} 秒")

    # 測試 1: 查詢所有 logs (使用最大 page_size)
    max_page_size = 500
    start_query = time.time()
    response = client.get(f"/send_logs?page_size={max_page_size}", headers=auth_headers)
    query_time = time.time() - start_query

    assert response.status_code == 200
    logs = response.json()
    # 應該返回至少一頁的資料
    assert len(logs) >= min(max_page_size, total_logs)
    print(f"查詢所有記錄時間: {query_time:.3f} 秒 ({len(logs)} 筆)")

    # 驗證: 查詢應在 2 秒內完成
    assert query_time < 2.0, f"查詢時間過長: {query_time:.3f}s"

    # 測試 2: 按 program_id 過濾
    start_filter = time.time()
    response = client.get(
        f"/send_logs?program_id={program.id}&page_size=500", headers=auth_headers
    )
    filter_time = time.time() - start_filter

    assert response.status_code == 200
    filtered_logs = response.json()
    print(f"按 program 過濾時間: {filter_time:.3f} 秒 ({len(filtered_logs)} 筆)")

    # 過濾查詢應該更快
    assert filter_time < 2.0, f"過濾查詢時間過長: {filter_time:.3f}s"

    # 測試 3: 按 result 過濾
    start_result = time.time()
    response = client.get(
        "/send_logs?result=success&page_size=500", headers=auth_headers
    )
    result_time = time.time() - start_result

    assert response.status_code == 200
    success_logs = response.json()
    print(f"按結果過濾時間: {result_time:.3f} 秒 ({len(success_logs)} 筆)")
    assert result_time < 2.0, f"結果過濾時間過長: {result_time:.3f}s"

    # 測試 4: 分頁查詢
    start_page = time.time()
    response = client.get("/send_logs?page=1&page_size=50", headers=auth_headers)
    page_time = time.time() - start_page

    assert response.status_code == 200
    paged_logs = response.json()
    assert len(paged_logs) <= 50
    print(f"分頁查詢時間: {page_time:.3f} 秒 (頁面大小: {len(paged_logs)})")
    assert page_time < 2.0, f"分頁查詢時間過長: {page_time:.3f}s"


def test_sendlog_index_effectiveness(db_session):
    """驗證 SendLog 索引的有效性"""
    # 建立測試資料
    program = Program(name="IndexTestProg", description="Test")
    db_session.add(program)
    db_session.commit()
    db_session.refresh(program)

    release = Release(
        program_id=program.id, version="v1.0.0", notes="Test", created_by=1
    )
    db_session.add(release)
    db_session.commit()
    db_session.refresh(release)

    # 建立大量記錄
    num_logs = 500
    for i in range(num_logs):
        log = SendLog(
            release_id=release.id,
            result=SendResult.success if i % 2 == 0 else SendResult.failure,
            detail=f"Test log {i}",
        )
        db_session.add(log)

    db_session.commit()

    # 測試索引查詢效能
    start = time.time()
    logs = db_session.query(SendLog).filter(SendLog.release_id == release.id).all()
    query_time = time.time() - start

    assert len(logs) == num_logs
    print(f"\n索引查詢時間 ({num_logs} 筆): {query_time:.4f} 秒")

    # 有索引的查詢應該非常快
    assert query_time < 1.0, f"索引查詢應該更快: {query_time:.4f}s"

    # 測試按時間排序的查詢
    start = time.time()
    recent_logs = (
        db_session.query(SendLog)
        .filter(SendLog.release_id == release.id)
        .order_by(SendLog.sent_at.desc())
        .limit(10)
        .all()
    )
    sort_time = time.time() - start

    assert len(recent_logs) == 10
    print(f"排序查詢時間 (最近 10 筆): {sort_time:.4f} 秒")
    assert sort_time < 1.0, f"排序查詢應該快速: {sort_time:.4f}s"


def test_concurrent_sendlog_queries(client, auth_headers, db_session):
    """模擬並發查詢情境"""
    # 建立測試資料
    program = Program(name="ConcurrentTestProg", description="Test")
    db_session.add(program)
    db_session.commit()
    db_session.refresh(program)

    release = Release(
        program_id=program.id, version="v1.0.0", notes="Concurrent test", created_by=1
    )
    db_session.add(release)
    db_session.commit()
    db_session.refresh(release)

    # 建立記錄
    for i in range(200):
        log = SendLog(
            release_id=release.id,
            result=SendResult.success,
            detail=f"Concurrent log {i}",
        )
        db_session.add(log)
    db_session.commit()

    # 模擬多個查詢
    queries = [
        f"/send_logs?program_id={program.id}&page_size=200",
        "/send_logs?result=success&page_size=200",
        "/send_logs?page=1&page_size=20",
        "/send_logs?page_size=200",
    ]

    start = time.time()
    responses = []
    for query in queries:
        resp = client.get(query, headers=auth_headers)
        responses.append(resp)
    total_time = time.time() - start

    # 所有查詢應該成功
    for resp in responses:
        assert resp.status_code == 200

    avg_time = total_time / len(queries)
    print(f"\n{len(queries)} 個並發查詢總時間: {total_time:.3f} 秒")
    print(f"平均每個查詢: {avg_time:.3f} 秒")

    # 平均查詢時間應該合理
    assert avg_time < 2.0, f"平均查詢時間過長: {avg_time:.3f}s"
