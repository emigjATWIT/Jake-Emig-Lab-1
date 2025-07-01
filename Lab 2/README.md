
---

## Lab 2 (CLI Driver, Unit Testing, Headers & Cookies)

### Command-Line Interface Driver (cli_driver.py)
A CLI tool was added to simulate a user calling all routes. It uses Python's `requests` library to send HTTP requests to the running FastAPI server and print responses.

**To run:**
1. Start the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```
2. In a new terminal:
   ```bash
   python cli_driver.py
   ```

---

### Unit Tests with `unittest` (test_main.py)
A full suite of unit tests was added using Python’s built-in `unittest` module and FastAPI’s `TestClient`.

**To run:**
```bash
python -m unittest test_main.py
```

Tests validate:
- All basic routes return correct structure/data
- Header and Cookie route handling
- Valid response formats and keys

---

### New Routes Added

#### Header Parameter Route
```python
@app.get("/header-test")
def header_test(x_campus: str = Header(...)):
    return {"X-Campus": x_campus}
```
Tested in CLI and unit tests using a custom `X-Campus` header.

#### Cookie Parameter Route
```python
@app.get("/cookie-test")
def cookie_test(session_id: str = Cookie(default="none")):
    return {"session_id": session_id}
```
Accepts cookies and confirms session value — also included in tests and CLI.

---

These additions enhance the application’s realism, simulate client-side usage, and ensure all routes are properly validated.
