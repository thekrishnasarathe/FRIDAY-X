import os
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.agent_tools import tool_system_diagnostics, tool_memory_manager

client = TestClient(app)


def test_streaming_endpoint():
    """Verify /chat/stream returns valid text/event-stream chunks."""
    payload = {"message": "hello streaming agent", "mode": "assistant"}
    response = client.post("/chat/stream", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")
    
    body = response.text
    assert "data:" in body
    assert "token" in body or "status" in body or "done" in body


def test_tool_system_diagnostics_nonzero_resilience():
    """Verify diagnostics tool never returns stuck 0.0 values even in container environments."""
    diag = tool_system_diagnostics()
    assert diag["status"] == "ONLINE"
    assert diag["cpu"] > 0
    assert diag["ram"] > 0
    assert diag["latency_ms"] > 0
    assert "CPU" in diag["summary"]


def test_telemetry_endpoint():
    """Verify /automation/telemetry returns structured gauges & sparkline arrays."""
    response = client.get("/automation/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data and data["cpu"] > 0
    assert "ram" in data and data["ram"] > 0
    assert "latency" in data and data["latency"] > 0
    assert "sparklines" in data
    assert len(data["sparklines"]["cpu"]) == 8


def test_memory_crud_endpoints():
    """Verify memory manager save, list, and delete workflow."""
    # 1. Add memory
    add_res = client.post("/memory/add", json={"key": "preferred_language", "value": "Python & React"})
    assert add_res.status_code == 200
    
    # 2. List memories
    list_res = client.get("/memory/list")
    assert list_res.status_code == 200
    memories = list_res.json()
    assert "facts" in memories
    assert "preferred_language" in memories["facts"]

    # 3. Delete memory
    del_res = client.delete("/memory/delete/preferred_language")
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "deleted"


def test_health_granular_diagnostics():
    """Verify enhanced /health returns granular telemetry and provider metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "llm_provider" in data
    assert "available_modules" in data
    assert "uptime_seconds" in data
    assert len(data["available_modules"]) >= 5
