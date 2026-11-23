import os
import pytest
from fastapi.testclient import TestClient

# Ensure offline deterministic mode for fast tests without network waits
os.environ["GROQ_API_KEY"] = ""

from app.main import app

client = TestClient(app)


def test_health_check():
    """Verify /health returns 200 with healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert data.get("health") == "ok"
    assert "service" in data


def test_root_endpoint():
    """Verify / returns service overview and endpoints list."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "online"
    assert "version" in data
    assert "endpoints" in data


def test_chat_trailing_and_non_trailing_slash(monkeypatch):
    """Verify both /chat and /chat/ accept POST without 307 redirects."""
    import app.core.response_engine as re_engine
    monkeypatch.setattr(re_engine, "chat_with_ai", lambda msg, history=None: f"FRIDAY echo: {msg}")

    payload = {"message": "hello friday", "speak": False}
    
    res_slash = client.post("/chat/", json=payload)
    assert res_slash.status_code == 200
    assert "friday_response" in res_slash.json()

    res_no_slash = client.post("/chat", json=payload)
    assert res_no_slash.status_code == 200
    assert "friday_response" in res_no_slash.json()


def test_chat_offline_fallback_resilience():
    """Verify chat never crashes with 500 even without external LLM."""
    payload = {"message": "kya haal hai", "speak": False}
    response = client.post("/chat/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("friday_response", "")) > 0


def test_automation_execute():
    """Verify automation execute endpoint returns command result."""
    response = client.get("/automation/execute", params={"command": "system status"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert len(data["result"]) > 0


def test_security_status():
    """Verify security status returns current security posture."""
    response = client.get("/security/status")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data


def test_memory_history():
    """Verify memory history returns history list."""
    response = client.get("/memory/history")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert isinstance(data["history"], list)


def test_cors_headers():
    """Verify CORS preflight OPTIONS returns allowed headers."""
    response = client.options(
        "/chat/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
