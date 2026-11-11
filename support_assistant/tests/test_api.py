from fastapi.testclient import TestClient
from support_assistant.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_ask_policy():
    response = client.post("/ask", json={"query": "What is the return policy duration?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert data["intent"] == "policy_rag"