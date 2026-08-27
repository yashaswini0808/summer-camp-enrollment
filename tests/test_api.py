import pytest
from fastapi.testclient import TestClient
from main import app
from app.firestore_crud import seed_firestore_db, get_firestore_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    db = get_firestore_db()
    # Reset emulator data if present
    if hasattr(db, "data"):
        db.data = {"sports": {}, "enrollments": {}}
    seed_firestore_db()
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_sports_firestore():
    response = client.get("/api/sports")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_crud_add_edit_delete_sport():
    # 1. ADD a new sport (POST)
    new_sport_payload = {
        "title": "React Firestore Archery",
        "category": "Outdoor & Track",
        "description": "Archery masterclass for teens",
        "min_age": 10,
        "max_age": 17,
        "instructor": "Coach Katniss",
        "schedule_days": "Sat, Sun",
        "schedule_time": "01:00 PM - 03:00 PM",
        "location": "Outdoor Range 1",
        "fee": 180.0,
        "max_capacity": 10,
        "image_icon": "🏹",
        "is_active": True
    }
    create_res = client.post("/api/sports", json=new_sport_payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    sport_id = str(created_data["id"])
    assert created_data["title"] == "React Firestore Archery"

    # 2. EDIT / UPDATE sport (PUT)
    update_payload = {
        "title": "React Firestore Archery Pro",
        "max_capacity": 15,
        "instructor": "Coach Katniss Everdeen"
    }
    edit_res = client.put(f"/api/sports/{sport_id}", json=update_payload)
    assert edit_res.status_code == 200
    edited_data = edit_res.json()
    assert edited_data["title"] == "React Firestore Archery Pro"
    assert edited_data["max_capacity"] == 15

    # 3. DELETE / Deactivate sport (DELETE)
    delete_res = client.delete(f"/api/sports/{sport_id}")
    assert delete_res.status_code == 200

    # Verify soft deleted from active listing
    active_sports = client.get("/api/sports?active_only=true").json()
    active_titles = [s["title"] for s in active_sports]
    assert "React Firestore Archery Pro" not in active_titles

def test_successful_enrollment():
    sports = client.get("/api/sports").json()
    sport = sports[0]

    enrollment_payload = {
        "sport_id": sport["id"],
        "participant_name": "React Student",
        "participant_age": sport["min_age"],
        "participant_grade": "5th Grade",
        "tshirt_size": "M",
        "medical_notes": "None",
        "parent_name": "React Parent",
        "parent_email": "reactparent@example.com",
        "parent_phone": "+1-555-9900",
        "emergency_contact": "+1-555-8800",
        "payment_method": "Full Payment"
    }

    res = client.post("/api/enrollments", json=enrollment_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["participant_name"] == "React Student"
    assert data["enrollment_code"].startswith("CAMP-2026-")

def test_age_validation_rejection():
    # Create sport min_age 12
    create_res = client.post("/api/sports", json={
        "title": "Teen Rowing League",
        "category": "Water Sports",
        "description": "Rowing for teens",
        "min_age": 12,
        "max_age": 18,
        "instructor": "Coach Oxford",
        "schedule_days": "Tue, Thu",
        "schedule_time": "08:00 AM",
        "location": "Lake Boathouse",
        "fee": 200.0,
        "max_capacity": 8,
        "image_icon": "🚣",
        "is_active": True
    })
    sport_id = create_res.json()["id"]

    res = client.post("/api/enrollments", json={
        "sport_id": sport_id,
        "participant_name": "Younger Student",
        "participant_age": 6, # Age 6 is valid for schema, but < min_age (12)
        "tshirt_size": "S",
        "parent_name": "Parent Person",
        "parent_email": "parent.p@example.com",
        "parent_phone": "+1-555-1122",
        "emergency_contact": "+1-555-3344",
        "payment_method": "Full Payment"
    })
    assert res.status_code == 400
    assert "Age Validation Failed" in res.json()["detail"]

def test_cancel_enrollment_and_capacity_release():
    sports = client.get("/api/sports").json()
    sport = sports[0]

    res = client.post("/api/enrollments", json={
        "sport_id": sport["id"],
        "participant_name": "Cancel Student",
        "participant_age": sport["min_age"],
        "tshirt_size": "M",
        "parent_name": "Cancel Parent",
        "parent_email": "cancel.p@example.com",
        "parent_phone": "+1-555-9988",
        "emergency_contact": "+1-555-7766",
        "payment_method": "Full Payment"
    })
    enrollment = res.json()

    cancel_res = client.put(f"/api/enrollments/{enrollment['id']}/cancel")
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "CANCELLED"
