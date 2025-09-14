import json


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data.get("status") == "ok"
