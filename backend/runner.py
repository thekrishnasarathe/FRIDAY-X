import requests
import json
import time
import urllib.parse

BASE_URL = "http://127.0.0.1:8000"

print("=" * 55)
print("  FRIDAY-X  --  Extreme Integration Test Suite")
print("=" * 55 + "\n")

passed = 0
failed = 0
total_time = 0

def run_test(name, func):
    global passed, failed, total_time
    try:
        print(f"  [{passed+failed+1:02d}] {name}...", end=" ")
        t0 = time.time()
        func()
        dt = time.time() - t0
        total_time += dt
        print(f"PASS  ({dt:.2f}s)")
        passed += 1
    except Exception as e:
        dt = time.time() - t0
        total_time += dt
        print(f"FAIL  ({dt:.2f}s) -> {e}")
        failed += 1

# ===== 1. SYSTEM ENDPOINTS =====
print("--- System Endpoints ---")

def t_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def t_root():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    d = r.json()
    assert "version" in d
    assert d["status"] == "online"

run_test("Health Check", t_health)
run_test("Root / System Info", t_root)

# ===== 2. CHAT (Groq LLM) =====
print("\n--- Chat / AI (Groq) ---")

def t_chat_joke():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "tell me a joke", "speak": False})
    assert r.status_code == 200
    d = r.json()
    assert "friday_response" in d and len(d["friday_response"]) > 5

def t_chat_greeting():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "hello friday", "speak": False})
    assert r.status_code == 200
    d = r.json()
    assert "friday_response" in d and len(d["friday_response"]) > 2

def t_chat_identity():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "who are you", "speak": False})
    assert r.status_code == 200
    d = r.json()
    assert "friday_response" in d

def t_chat_hinglish():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "kya haal hai bhai", "speak": False})
    assert r.status_code == 200
    d = r.json()
    assert "friday_response" in d and len(d["friday_response"]) > 2

run_test("Chat - Tell a joke (LLM)", t_chat_joke)
run_test("Chat - Greeting", t_chat_greeting)
run_test("Chat - Identity (who are you)", t_chat_identity)
run_test("Chat - Hinglish support", t_chat_hinglish)

# ===== 3. COMMANDS VIA CHAT (intent routing) =====
print("\n--- Command Routing via /chat/ ---")

def t_cmd_time():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "what time is it", "speak": False})
    assert r.status_code == 200
    d = r.json()
    resp = d.get("friday_response", "").lower()
    assert any(w in resp for w in ["time", ":", "am", "pm", "hour"]), f"Unexpected: {resp[:80]}"

def t_cmd_weather():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "weather in London", "speak": False})
    assert r.status_code == 200
    d = r.json()
    resp = d.get("friday_response", "").lower()
    assert any(w in resp for w in ["weather", "london", "c", "f"]), f"Unexpected: {resp[:80]}"

def t_cmd_news():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "show me the news", "speak": False})
    assert r.status_code == 200
    d = r.json()
    resp = d.get("friday_response", "")
    assert len(resp) > 10, f"Response too short: {resp[:60]}"

def t_cmd_system():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "system status", "speak": False})
    assert r.status_code == 200
    d = r.json()
    resp = d.get("friday_response", "").lower()
    assert any(w in resp for w in ["cpu", "ram", "battery", "%"]), f"Unexpected: {resp[:80]}"

def t_cmd_battery():
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "battery status", "speak": False})
    assert r.status_code == 200
    d = r.json()
    resp = d.get("friday_response", "").lower()
    assert any(w in resp for w in ["battery", "%"]), f"Unexpected: {resp[:80]}"

run_test("Cmd - Time/Date", t_cmd_time)
run_test("Cmd - Weather (cached)", t_cmd_weather)
run_test("Cmd - News (cached)", t_cmd_news)
run_test("Cmd - System Status (cached)", t_cmd_system)
run_test("Cmd - Battery Status", t_cmd_battery)

# ===== 4. CACHING VERIFICATION =====
print("\n--- Cache Performance ---")

def t_cache_weather():
    """Second weather call should be near-instant from cache."""
    # Prime the cache
    requests.post(f"{BASE_URL}/chat/", json={"message": "weather in London", "speak": False})
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "weather in London", "speak": False})
    dt = time.time() - t0
    assert r.status_code == 200
    assert dt < 3.0, f"Cache miss - took {dt:.2f}s, expected < 3s"

def t_cache_system():
    """Second system status call should use 10s cache."""
    requests.post(f"{BASE_URL}/chat/", json={"message": "system status", "speak": False})
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/chat/", json={"message": "system status", "speak": False})
    dt = time.time() - t0
    assert r.status_code == 200
    assert dt < 2.0, f"Cache miss - took {dt:.2f}s, expected < 2s"

run_test("Cache - Weather (repeat call)", t_cache_weather)
run_test("Cache - System (repeat call)", t_cache_system)

# ===== 5. AUTOMATION DIRECT =====
print("\n--- Direct Automation Endpoint ---")

def t_auto_direct():
    r = requests.get(f"{BASE_URL}/automation/execute", params={"command": "system status"})
    assert r.status_code == 200

run_test("Automation /execute endpoint", t_auto_direct)

# ===== 6. OTHER ROUTES (existence check) =====
print("\n--- Route Existence ---")

def t_route(path):
    def check():
        r = requests.get(f"{BASE_URL}{path}")
        assert r.status_code in (200, 405, 422), f"Got {r.status_code}"
    return check

run_test("Route - /memory/history", t_route("/memory/history"))
run_test("Route - /docs (Swagger)", t_route("/docs"))

# ===== SUMMARY =====
print("\n" + "=" * 55)
print(f"  RESULTS: {passed} passed / {failed} failed / {passed+failed} total")
print(f"  Total time: {total_time:.2f}s")
print("=" * 55)
