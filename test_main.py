
import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestCollegeLifeAPI(unittest.TestCase):

    def test_root(self):
        r = client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_motivation(self):
        r = client.get("/motivation")
        self.assertIn("quote", r.json())

    def test_student(self):
        r = client.get("/student/1")
        self.assertIn("name", r.json())

    def test_cafeteria(self):
        r = client.get("/cafeteria/monday")
        self.assertIsInstance(r.json()["menu"], list)

    def test_class(self):
        r = client.get("/class/COMP101")
        self.assertIn("title", r.json())

    def test_gpa(self):
        r = client.get("/gpa?grades=A,B,C")
        self.assertIn("gpa", r.json())

    def test_studytime(self):
        r = client.get("/studytime?hours=3")
        self.assertIn("message", r.json())

    def test_events(self):
        r = client.get("/events?club=test")
        self.assertIn("events", r.json())

    def test_sleepcheck(self):
        r = client.get("/sleepcheck?hours=6")
        self.assertIn("message", r.json())

    def test_resources(self):
        r = client.get("/resources")
        self.assertIsInstance(r.json()["campus_resources"], list)

    def test_header_param(self):
        r = client.get("/header-test", headers={"X-Campus": "North"})
        self.assertIn("X-Campus", r.json())

    def test_cookie_param(self):
        r = client.get("/cookie-test", cookies={"session_id": "abc123"})
        self.assertIn("session_id", r.json())

if __name__ == "__main__":
    unittest.main()
