from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
    )

    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_duplicate_signup_is_case_insensitive():
    activity_name = "Programming Class"
    email = "CaseTest@Mergington.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/activities/{activity_name}/signup?email=casetest@mergington.edu",
    )

    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()
