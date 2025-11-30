import concurrent.futures
from fastapi.testclient import TestClient
from app.main import app

def send_request():
    local_client = TestClient(app)  # ✅ UN CLIENT PAR THREAD
    return local_client.post(
        "/reservations",
        json={
            "showtime_id": 1,
            "seat_number": "A1"
        },
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3NjQ1NDk3NTl9.5DDftU3XUXf_vIcyjaLLxSGMwzKcwc5AusBJSS7dXwg"
        }
    )

def test_concurrent_reservations():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: send_request(), range(10)))

    success = [r for r in results if r.status_code == 200]
    failed = [r for r in results if r.status_code in (400, 409)]

    assert len(success) == 1
    assert len(failed) == 9
