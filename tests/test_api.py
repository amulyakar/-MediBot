
from types import SimpleNamespace

from fastapi.testclient import TestClient

import app.main as main_module


client = TestClient(main_module.app)


# TEST 1: Homepage
def test_homepage():

    response = client.get("/")

    assert response.status_code == 200
    assert "MediBot" in response.text


# TEST 2: Health Check
def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["app_name"] == "MediBot"


# TEST 3: Ask Question
def test_ask_question(monkeypatch):

    # Create a fake AI team response.
    # This prevents an actual Groq API call during testing.
    class FakeMedicalTeam:

        def run(self, question):

            return SimpleNamespace(
                content="The common cold is a viral infection."
            )

    # Temporarily replace the real AI team with the fake team
    monkeypatch.setattr(
        main_module,
        "medical_team",
        FakeMedicalTeam()
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is the common cold?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What is the common cold?"
    assert "viral infection" in data["answer"]
    assert "educational information only" in data["disclaimer"]


# TEST 4: Invalid Question
def test_invalid_question():

    response = client.post(
        "/ask",
        json={
            "question": "Hi"
        }
    )

    assert response.status_code == 422
