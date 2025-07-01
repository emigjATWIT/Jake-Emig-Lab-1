
# College Life API


A humorous and helpful API simulating the daily struggles (and wins) of college student life built with FastAPI.

---

## Introduction

Welcome to the **College Life API** — a lightweight web service that emulates the chaos of student routines using RESTful routes. From checking the cafeteria menu to figuring out your GPA (or lack thereof), this API gives you a mock interface to interact with student life programmatically.

---

## Features

- **10+ Routes** — Combining simple, path, and query string examples
- **Random motivational quotes**
- **Daily cafeteria menus**
- **Course information lookup**
- **GPA calculator**
- **Study and sleep advice**
- **Mock student profiles**
- Fully interactive Swagger docs

---

## Project Design

The project uses:

- [FastAPI](https://fastapi.tiangolo.com/) for route handling and performance
- `uvicorn` for serving the app
- Simple Python dictionaries to simulate data storage

### Route Breakdown

| Route                  | Method | Type       | Description                          |
|------------------------|--------|------------|--------------------------------------|
| `/`                    | GET    | Simple     | Welcome message                      |
| `/motivation`          | GET    | Simple     | Random quote                         |
| `/student/{id}`        | GET    | Path       | Returns student data                 |
| `/cafeteria/{day}`     | GET    | Path       | Shows menu for a given weekday       |
| `/class/{course_code}` | GET    | Path       | Course information                   |
| `/gpa?grades=`         | GET    | Query      | GPA calculation from letter grades   |
| `/studytime?hours=`    | GET    | Query      | Motivation based on study time       |
| `/events?club=`        | GET    | Query      | Club event info                      |
| `/sleepcheck?hours=`   | GET    | Query      | Sleep health feedback                |
| `/resources`           | GET    | Simple     | List of campus support services      |

---

## Getting Started

### Prerequisites

- Python 3.9+
- FastAPI and Uvicorn

### Installation

```bash
git clone https://github.com/your-username/college-life-api.git
cd college-life-api
pip install fastapi uvicorn
```

### Running the App

```bash
uvicorn main:app --reload
```

Then open your browser:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testing the API

You can manually test routes using:

- The `/docs` Swagger UI
- Python `requests` module
- Postman or cURL

Example Python test:
```python
import requests
print(requests.get("http://127.0.0.1:8000/motivation").json())
```

---

## Future Improvements

- Add SQLite/PostgreSQL backend
- Add user authentication
- Build a React-based frontend

---

## Author

**Jake Emig**

