from fastapi.testclient import TestClient
from app.main import app, engine

engine.mock_mode = True

with TestClient(app) as client:
    health = client.get("/health")
    assert health.status_code == 200
    payload = {
        "boardSize": 19,
        "moves": [["B", "Q16"], ["W", "D4"]],
        "initialStones": [],
        "komi": 6.5,
        "rules": "japanese",
        "maxVisits": 100,
        "includePolicy": True,
        "includeOwnership": True,
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert 0 <= data["blackWinrate"] <= 1
    assert len(data["moveInfos"]) >= 1
    print("Build017.3 mock server test passed")
