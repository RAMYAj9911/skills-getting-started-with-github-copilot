import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    # Arrange
    # ...nothing to arrange for GET...
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Clean up
    activities[activity_name]["participants"].remove(email)

def test_duplicate_signup():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@mergington.edu"
    activities[activity_name]["participants"].append(email)
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    # Clean up
    activities[activity_name]["participants"].remove(email)

def test_unregister_for_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@mergington.edu"
    activities[activity_name]["participants"].append(email)
    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

def test_unregister_non_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
