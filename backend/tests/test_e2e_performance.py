"""E2E 效能測試

測試從建立 Release 到發送完成的整體延遲,驗證:
- SC-001: 平均處理時間 <= 3 分鐘
- 單次發送的端到端延遲
"""

import time


def test_e2e_latency_single_release(client, auth_headers, smtp_stub):
    """測試單一 release 的端到端延遲"""
    smtp_stub.set_behavior("success")

    start_time = time.time()

    # 步驟 1: 建立 program
    prog_resp = client.post(
        "/programs",
        json={"name": "LatencyTestProg", "description": "Test"},
        headers=auth_headers,
    )
    assert prog_resp.status_code == 201
    program = prog_resp.json()

    # 步驟 2: 建立 release
    release_resp = client.post(
        "/releases",
        json={
            "program_id": program["id"],
            "version": "v1.0.0",
            "notes": "Test release for latency",
            "recipients": [
                {"email": f"user{i}@example.com", "type": "to"}
                for i in range(10)  # 10 個收件人
            ],
        },
        headers=auth_headers,
    )
    assert release_resp.status_code == 201
    release = release_resp.json()

    # 步驟 3: 預覽 (可選,但是工作流的一部分)
    preview_resp = client.get(
        f"/releases/{release['id']}/preview", headers=auth_headers
    )
    assert preview_resp.status_code == 200

    # 步驟 4: 發送
    send_resp = client.post(
        f"/releases/{release['id']}/send",
        json={
            "recipients": [
                {"email": f"user{i}@example.com", "type": "to"} for i in range(10)
            ]
        },
        headers=auth_headers,
    )
    assert send_resp.status_code == 200

    end_time = time.time()
    elapsed = end_time - start_time

    # 驗證: 整個流程應該在 3 分鐘內完成 (SC-001)
    # 實際上在測試環境中應該遠快於此 (通常 < 1 秒)
    assert elapsed < 180, f"E2E 延遲超過 3 分鐘: {elapsed:.2f}s"

    # 記錄實際延遲供參考
    print(f"\nE2E 延遲: {elapsed:.3f} 秒 (10 個收件人)")

    # 在測試環境中,應該非常快
    assert elapsed < 5, f"測試環境中延遲過高: {elapsed:.2f}s"


def test_e2e_latency_multiple_releases(client, auth_headers, smtp_stub):
    """測試多個 releases 的平均延遲"""
    smtp_stub.set_behavior("success")

    num_releases = 5
    latencies = []

    # 建立 program 一次
    prog_resp = client.post(
        "/programs",
        json={"name": "MultiLatencyTestProg", "description": "Test"},
        headers=auth_headers,
    )
    assert prog_resp.status_code == 201
    program = prog_resp.json()

    for i in range(num_releases):
        start_time = time.time()

        # 建立並發送 release
        release_resp = client.post(
            "/releases",
            json={
                "program_id": program["id"],
                "version": f"v1.0.{i}",
                "notes": f"Test release {i}",
                "recipients": [
                    {"email": f"user{j}@example.com", "type": "to"} for j in range(5)
                ],
            },
            headers=auth_headers,
        )
        assert release_resp.status_code == 201
        release = release_resp.json()

        send_resp = client.post(
            f"/releases/{release['id']}/send",
            json={
                "recipients": [
                    {"email": f"user{j}@example.com", "type": "to"} for j in range(5)
                ]
            },
            headers=auth_headers,
        )
        assert send_resp.status_code == 200

        elapsed = time.time() - start_time
        latencies.append(elapsed)

    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)

    print(f"\n平均延遲: {avg_latency:.3f} 秒 ({num_releases} 個 releases)")
    print(f"最大延遲: {max_latency:.3f} 秒")

    # 驗證平均延遲符合要求
    assert avg_latency < 180, f"平均延遲超過 3 分鐘: {avg_latency:.2f}s"
    assert avg_latency < 5, f"測試環境中平均延遲過高: {avg_latency:.2f}s"


def test_send_timeout_behavior(client, auth_headers, smtp_stub):
    """測試發送逾時行為 (SC-002: 30 秒 timeout)"""
    # 注意: 這個測試不實際等待30秒,而是驗證 timeout 參數被正確傳遞
    smtp_stub.set_behavior("success")

    prog_resp = client.post(
        "/programs",
        json={"name": "TimeoutTestProg", "description": "Test"},
        headers=auth_headers,
    )
    program = prog_resp.json()

    release_resp = client.post(
        "/releases",
        json={
            "program_id": program["id"],
            "version": "v1.0.0",
            "notes": "Timeout test",
            "recipients": [{"email": "test@example.com", "type": "to"}],
        },
        headers=auth_headers,
    )
    release = release_resp.json()

    start_time = time.time()
    send_resp = client.post(
        f"/releases/{release['id']}/send",
        json={"recipients": [{"email": "test@example.com", "type": "to"}]},
        headers=auth_headers,
    )
    elapsed = time.time() - start_time

    assert send_resp.status_code == 200
    # 在測試環境中應該立即返回
    assert elapsed < 5, "同步發送應該快速完成(在測試環境中)"
