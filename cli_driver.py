
import requests

BASE_URL = "http://127.0.0.1:8000"

def call_route(endpoint, headers=None, cookies=None):
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, cookies=cookies)
    print(f"GET {endpoint} -> {response.status_code}")
    print(response.json())

def main():
    print("📡 Calling College Life API Routes...")
    call_route("/")
    call_route("/motivation")
    call_route("/student/1")
    call_route("/cafeteria/monday")
    call_route("/class/COMP101")
    call_route("/gpa?grades=A,B,C")
    call_route("/studytime?hours=4")
    call_route("/events?club=gaming")
    call_route("/sleepcheck?hours=6")
    call_route("/resources")
    call_route("/header-test", headers={"X-Campus": "North"})
    call_route("/cookie-test", cookies={"session_id": "abc123"})

if __name__ == "__main__":
    main()
