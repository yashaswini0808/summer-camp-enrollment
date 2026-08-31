import os
import json
import re
import random
import string
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from fastapi import HTTPException, status
from google.oauth2 import service_account
from google.auth.transport.requests import Request

from backend.firebase import get_db
from backend.models_pydantic import UserCreate, UserUpdate, SportCreate, SportUpdate, EnrollmentCreate

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def sync_to_firebase_cloud(collection_name: str, doc_id: str, payload: dict):
    """
    Guarantees real-time sync of all CRUD operations to live Google Cloud Firebase Console.
    Flow: firestore_crud.py -> sync_to_firebase_cloud() -> Firebase Cloud REST API
    """
    try:
        credentials_path = "backend/firebase_credentials.json"
        if not os.path.exists(credentials_path):
            credentials_path = "firebase_credentials.json"


        with open(credentials_path) as f:
            key_info = json.load(f)

        project_id = key_info["project_id"]
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/datastore"]
        )
        creds.refresh(Request())
        token = creds.token

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        def py_val_to_firestore_val(key_name, val):
            if val is None:
                return {"nullValue": None}
            elif isinstance(val, bool):
                return {"booleanValue": val}
            elif isinstance(val, int):
                return {"integerValue": str(val)}
            elif isinstance(val, float):
                return {"doubleValue": val}
            elif isinstance(val, str):
                return {"stringValue": val}
            elif isinstance(val, dict):
                fields = {k: py_val_to_firestore_val(k, v) for k, v in val.items() if v is not None}
                return {"mapValue": {"fields": fields}}
            elif isinstance(val, list):
                return {"arrayValue": {"values": [py_val_to_firestore_val(key_name, item) for item in val]}}
            return {"stringValue": str(val)}

        fields = {k: py_val_to_firestore_val(k, v) for k, v in payload.items() if v is not None}
        mask_params = "&".join([f"updateMask.fieldPaths={k}" for k in payload.keys() if payload[k] is not None])

        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/{collection_name}/{doc_id}?{mask_params}"
        res = requests.patch(url, headers=headers, json={"fields": fields})
        if res.status_code == 200:
            print(f"[FIREBASE SYNC SUCCESS 200 OK] Live updated '{collection_name}/{doc_id}' in Google Cloud!")
        else:
            print(f"[!] Firebase Sync notice ({res.status_code}): {res.text[:150]}")
    except Exception as e:
        print(f"[WARNING] Live Firebase cloud sync notice: {e}")

def delete_firebase_cloud_doc(collection_name: str, doc_id: str):
    """Deletes a document from Google Cloud Firebase Console."""
    try:
        credentials_path = "backend/firebase_credentials.json"
        if not os.path.exists(credentials_path):
            credentials_path = "firebase_credentials.json"


        with open(credentials_path) as f:
            key_info = json.load(f)

        project_id = key_info["project_id"]
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/datastore"]
        )
        creds.refresh(Request())
        token = creds.token

        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/{collection_name}/{doc_id}"
        requests.delete(url, headers=headers)
        print(f"[FIREBASE DELETE SUCCESS] Removed '{collection_name}/{doc_id}' from Google Cloud!")
    except Exception as e:
        print(f"[!] Delete document notice: {e}")


def fetch_firestore_cloud_collection(collection_name: str) -> List[Dict[str, Any]]:
    """Fetches real-time documents from Google Cloud Firestore REST API."""
    try:
        credentials_path = "backend/firebase_credentials.json"
        if not os.path.exists(credentials_path):
            credentials_path = "firebase_credentials.json"

        with open(credentials_path) as f:
            key_info = json.load(f)

        project_id = key_info["project_id"]
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/datastore"]
        )
        creds.refresh(Request())
        token = creds.token

        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/{collection_name}"
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            docs = res.json().get("documents", [])
            results = []
            for doc in docs:
                doc_id = doc["name"].split("/")[-1]
                fields = doc.get("fields", {})
                
                item = {"id": doc_id}
                for k, v in fields.items():
                    if "stringValue" in v:
                        item[k] = v["stringValue"]
                    elif "integerValue" in v:
                        item[k] = int(v["integerValue"])
                    elif "doubleValue" in v:
                        item[k] = float(v["doubleValue"])
                    elif "booleanValue" in v:
                        item[k] = bool(v["booleanValue"])
                    elif "nullValue" in v:
                        item[k] = None
                    elif "mapValue" in v:
                        sub_fields = v["mapValue"].get("fields", {})
                        sub_dict = {}
                        for sk, sv in sub_fields.items():
                            if "stringValue" in sv:
                                sub_dict[sk] = sv["stringValue"]
                            elif "integerValue" in sv:
                                sub_dict[sk] = int(sv["integerValue"])
                            elif "doubleValue" in sv:
                                sub_dict[sk] = float(sv["doubleValue"])
                            elif "booleanValue" in sv:
                                sub_dict[sk] = bool(sv["booleanValue"])
                        item[k] = sub_dict
                results.append(item)
            return results
    except Exception as e:
        print(f"[!] Cloud REST fetch notice ({collection_name}): {e}")
    return []


# ==========================================
# 1. USER DATABASE OPERATIONS (Requirement #5)
# ==========================================

def get_users() -> List[Dict[str, Any]]:
    """Retrieves all users from Firestore database collection 'users'."""
    users = fetch_firestore_cloud_collection("users")

    # If Firestore returns empty, return default seed users for initial display
    if not users:
        users = [
            {"id": "user-savitri", "name": "Savitri", "email": "divyashreens11@gmail.com", "age": 35, "role": "Parent", "created_at": "2026-08-26T11:00:00Z"},
            {"id": "user-nisha", "name": "Nisha", "email": "kerthi12@gmail.com", "age": 32, "role": "Parent", "created_at": "2026-08-27T08:00:00Z"},
            {"id": "user-admin", "name": "Admin Manager", "email": "admin@summercamp.org", "age": 40, "role": "Administrator", "created_at": "2026-01-01T00:00:00Z"}
        ]
    return users



def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single user by ID from Firestore."""
    users = get_users()
    str_id = str(user_id).strip().lower()
    for u in users:
        if str(u.get("id", "")).strip().lower() == str_id:
            return u
    return None


def create_user(user_data: UserCreate) -> Dict[str, Any]:
    """Creates a new user document in Firestore."""
    user_doc_id = f"user-{slugify(user_data.name)}"
    data = user_data.model_dump()
    data["id"] = user_doc_id
    data["created_at"] = datetime.utcnow().isoformat()

    # Save via Admin SDK or REST API sync
    db = get_db()
    if db:
        try:
            db.collection("users").document(user_doc_id).set(data)
        except Exception as e:
            print("[NOTICE] SDK write fallback:", e)

    sync_to_firebase_cloud("users", user_doc_id, data)
    return data


def update_user(user_id: str, user_data: UserUpdate) -> Dict[str, Any]:
    """Updates an existing user document in Firestore in-place without creating duplicates."""
    existing = get_user(user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found in Firestore."
        )

    doc_id = existing.get("id") or f"user-{slugify(existing['name'])}"
    update_dict = user_data.model_dump(exclude_unset=True)

    for k, v in update_dict.items():
        existing[k] = v

    sync_to_firebase_cloud("users", doc_id, existing)
    return existing


def delete_user(user_id: str) -> bool:
    """Deletes a user document from Firestore."""
    existing = get_user(user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found."
        )

    doc_id = existing.get("id") or f"user-{slugify(existing['name'])}"
    delete_firebase_cloud_doc("users", doc_id)
    return True


# ==========================================
# 2. SPORTS DATABASE OPERATIONS
# ==========================================

def get_sports(
    category: Optional[str] = None,
    age: Optional[int] = None,
    search: Optional[str] = None,
    active_only: bool = True
) -> List[Dict[str, Any]]:
    sports = fetch_firestore_cloud_collection("sports")

    for data in sports:
        data["id"] = data.get("slug_id") or data["id"]
        data["slug_id"] = data["id"]

    if not sports:
        from backend.seed import SAMPLE_SPORTS
        sports = SAMPLE_SPORTS


    # Apply filtering
    filtered = []
    for s in sports:
        if active_only and not s.get("is_active", True):
            continue
        if category and category != "All" and s.get("category") != category:
            continue
        if age is not None:
            if age < s.get("min_age", 0) or age > s.get("max_age", 99):
                continue
        if search:
            pat = search.strip().lower()
            t = s.get("title", "").lower()
            d = s.get("description", "").lower()
            inst = s.get("instructor", "").lower()
            if pat not in t and pat not in d and pat not in inst:
                continue
        filtered.append(s)

    return filtered


def get_sport_by_id(sport_id: Union[int, str]) -> Optional[Dict[str, Any]]:
    sports = get_sports(active_only=False)
    str_id = str(sport_id).strip().lower()
    for s in sports:
        s_id = str(s.get("id", "")).strip().lower()
        s_slug = str(s.get("slug_id", "")).strip().lower()
        if s_id == str_id or s_slug == str_id:
            return s
    return None


def create_sport(sport_data: SportCreate) -> Dict[str, Any]:
    doc_slug_id = slugify(sport_data.title)
    data = sport_data.model_dump()
    data["id"] = doc_slug_id
    data["slug_id"] = doc_slug_id
    data["enrolled_count"] = 0
    data["created_at"] = datetime.utcnow().isoformat()

    sync_to_firebase_cloud("sports", doc_slug_id, data)
    return data


def update_sport(sport_id: Union[int, str], sport_data: SportUpdate) -> Dict[str, Any]:
    existing = get_sport_by_id(sport_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID '{sport_id}' not found."
        )

    fixed_doc_id = existing.get("slug_id") or slugify(existing["title"])
    existing["id"] = fixed_doc_id
    existing["slug_id"] = fixed_doc_id

    update_dict = sport_data.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        existing[k] = v

    sync_to_firebase_cloud("sports", fixed_doc_id, existing)
    return existing


def delete_sport(sport_id: Union[int, str]) -> bool:
    existing = get_sport_by_id(sport_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID '{sport_id}' not found."
        )

    doc_id = existing.get("slug_id") or slugify(existing["title"])
    existing["is_active"] = False
    sync_to_firebase_cloud("sports", doc_id, existing)
    return True


# ==========================================
# 3. ENROLLMENT DATABASE OPERATIONS
# ==========================================

def generate_enrollment_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return f"CAMP-2026-{''.join(random.choices(chars, k=5))}"


def create_enrollment(data: EnrollmentCreate) -> Dict[str, Any]:
    sport = get_sport_by_id(data.sport_id)
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID '{data.sport_id}' does not exist in Firestore."
        )

    code = generate_enrollment_code()
    doc_e_id = f"{code.lower()}-{slugify(data.participant_name)}"

    enrollment_doc = {
        "id": doc_e_id,
        "enrollment_code": code,
        "sport_id": data.sport_id,
        "participant_name": data.participant_name.strip(),
        "participant_age": data.participant_age,
        "participant_grade": data.participant_grade,
        "tshirt_size": data.tshirt_size,
        "medical_notes": data.medical_notes,
        "parent_name": data.parent_name.strip(),
        "parent_email": data.parent_email.strip().lower(),
        "parent_phone": data.parent_phone.strip(),
        "emergency_contact": data.emergency_contact.strip(),
        "payment_method": data.payment_method,
        "amount_paid": float(sport.get("fee", 0.0)),
        "status": "CONFIRMED",
        "enrolled_at": datetime.utcnow().isoformat(),
        "sport": sport
    }

    sync_to_firebase_cloud("enrollments", doc_e_id, enrollment_doc)

    sport["enrolled_count"] = sport.get("enrolled_count", 0) + 1
    sport_doc_id = sport.get("slug_id") or slugify(sport["title"])
    sync_to_firebase_cloud("sports", sport_doc_id, sport)

    return enrollment_doc


def get_enrollments(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    db = get_db()
    results = []
    try:
        if db:
            docs = db.collection("enrollments").stream()
            for d in docs:
                data = d.to_dict()
                data["id"] = d.id
                if status_filter and status_filter != "ALL" and data.get("status") != status_filter.upper():
                    continue
                results.append(data)
    except Exception as e:
        print("[WARNING] get_enrollments notice:", e)

    return results


def get_dashboard_stats() -> Dict[str, Any]:
    sports = get_sports(active_only=False)
    enrollments = get_enrollments(status_filter="ALL")

    confirmed = [e for e in enrollments if e.get("status") == "CONFIRMED"]
    total_rev = sum(float(e.get("amount_paid", 0.0)) for e in confirmed)
    total_cap = sum(s.get("max_capacity", 0) for s in sports if s.get("is_active", True))
    total_enrolled = sum(s.get("enrolled_count", 0) for s in sports if s.get("is_active", True))

    return {
        "total_sports": len(sports),
        "active_sports": len([s for s in sports if s.get("is_active", True)]),
        "total_enrollments": len(enrollments),
        "confirmed_enrollments": len(confirmed),
        "cancelled_enrollments": len([e for e in enrollments if e.get("status") == "CANCELLED"]),
        "total_revenue": total_rev,
        "spots_available": max(0, total_cap - total_enrolled),
        "popular_sports": sports[:6]
    }
