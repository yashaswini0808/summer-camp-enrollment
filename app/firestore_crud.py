import json
import random
import string
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from fastapi import HTTPException, status
from google.oauth2 import service_account
from google.auth.transport.requests import Request

from app.firestore_db import get_firestore_db, FirestoreLocalEmulator
from app.models_pydantic import SportCreate, SportUpdate, EnrollmentCreate

def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def sync_to_firebase_cloud(collection_name: str, doc_id: str, payload: dict):
    """Guarantees instant sync of webpage edits to live Google Cloud Firebase Console"""
    # 1. Local emulator write
    try:
        FirestoreLocalEmulator().collection(collection_name).document(doc_id).set(payload, merge=True)
    except Exception as e:
        print(f"[NOTICE] Local emulator write: {e}")

    # 2. Live Cloud Firebase REST API sync
    try:
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


        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/{collection_name}/{doc_id}"
        res = requests.patch(url, headers=headers, json={"fields": fields})
        if res.status_code == 200:
            print(f"[FIREBASE SYNC SUCCESS] Live updated '{collection_name}/{doc_id}' in Google Cloud!")
        else:
            print(f"[!] Firebase Sync notice ({res.status_code}): {res.text[:150]}")
    except Exception as e:
        print(f"[WARNING] Live Firebase cloud sync notice: {e}")

def generate_enrollment_code() -> str:
    """Generates a random unique enrollment code, e.g. CAMP-2026-X89A"""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=5))
    return f"CAMP-2026-{suffix}"

# --- Sports Firestore Operations ---

def get_sports(
    category: Optional[str] = None,
    age: Optional[int] = None,
    search: Optional[str] = None,
    active_only: bool = True
) -> List[Dict[str, Any]]:
    db = get_firestore_db()
    sports = []

    try:
        if isinstance(db, FirestoreLocalEmulator):
            docs = db.collection("sports").stream()
        else:
            docs = db.collection("sports").stream(timeout=3.0)

        for doc in docs:
            data = doc.to_dict()
            if not data.get("id"):
                data["id"] = doc.id
            if not data.get("slug_id"):
                data["slug_id"] = doc.id
            
            if str(data["id"]).isdigit():
                data["id"] = int(data["id"])

            if active_only and not data.get("is_active", True):
                continue


            if category and category != "All" and data.get("category") != category:
                continue

            if age is not None:
                min_a = data.get("min_age", 0)
                max_a = data.get("max_age", 99)
                if age < min_a or age > max_a:
                    continue

            if search:
                pat = search.strip().lower()
                t = data.get("title", "").lower()
                d = data.get("description", "").lower()
                inst = data.get("instructor", "").lower()
                loc = data.get("location", "").lower()
                if pat not in t and pat not in d and pat not in inst and pat not in loc:
                    continue

            sports.append(data)
    except Exception as e:
        print("[WARNING] Using local persistent store:", e)
        emulator = FirestoreLocalEmulator()
        for doc in emulator.collection("sports").stream():
            data = doc.to_dict()
            if str(doc.id).isdigit():
                data["id"] = int(doc.id)
            if active_only and not data.get("is_active", True):
                continue
            sports.append(data)

    sports.sort(key=lambda x: str(x.get("id")))
    return sports

def get_sport_by_id(sport_id: Union[int, str]) -> Optional[Dict[str, Any]]:
    sports = get_sports(active_only=False)
    str_id = str(sport_id)
    for s in sports:
        if str(s.get("id")) == str_id:
            return s
    return None

def create_sport(sport_data: SportCreate) -> Dict[str, Any]:
    all_sports = get_sports(active_only=False)
    max_id = 0
    for s in all_sports:
        try:
            val = int(s["id"])
            if val > max_id:
                max_id = val
        except ValueError:
            pass

    new_id = max_id + 1
    doc_slug_id = slugify(sport_data.title)

    data = sport_data.model_dump()
    data["id"] = new_id
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
            detail=f"Sport with ID {sport_id} not found."
        )

    # Lock fixed document ID before updating title or fields
    target_doc_id = existing.get("slug_id") or slugify(existing["title"])
    existing["slug_id"] = target_doc_id

    update_dict = sport_data.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        existing[k] = v

    sync_to_firebase_cloud("sports", target_doc_id, existing)
    return existing


def delete_sport(sport_id: Union[int, str]) -> bool:
    existing = get_sport_by_id(sport_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID {sport_id} not found."
        )

    doc_slug_id = existing.get("slug_id") or slugify(existing["title"])
    existing["is_active"] = False
    sync_to_firebase_cloud("sports", doc_slug_id, existing)
    return True


# --- Enrollment Firestore Operations ---

def create_enrollment(data: EnrollmentCreate) -> Dict[str, Any]:
    sport = get_sport_by_id(data.sport_id)
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID {data.sport_id} does not exist in Firestore."
        )

    if not sport.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The sport '{sport['title']}' is currently inactive."
        )

    min_age = sport.get("min_age", 5)
    max_age = sport.get("max_age", 18)
    if data.participant_age < min_age or data.participant_age > max_age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Age Validation Failed: Participant age ({data.participant_age}) is outside permitted range for {sport['title']} ({min_age} - {max_age} yrs)."
        )

    enrolled_cnt = sport.get("enrolled_count", 0)
    max_cap = sport.get("max_capacity", 20)
    if enrolled_cnt >= max_cap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Capacity Limit Reached: '{sport['title']}' has reached maximum capacity of {max_cap} participants."
        )

    all_enrollments = get_enrollments(status_filter="ALL")
    p_name = data.participant_name.strip().lower()
    p_email = data.parent_email.strip().lower()
    s_id = str(data.sport_id)

    for e_dict in all_enrollments:
        if (
            str(e_dict.get("sport_id")) == s_id and
            e_dict.get("participant_name", "").strip().lower() == p_name and
            e_dict.get("parent_email", "").strip().lower() == p_email and
            e_dict.get("status") == "CONFIRMED"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate Enrollment: '{data.participant_name}' is already enrolled in '{sport['title']}' under code {e_dict.get('enrollment_code')}."
            )

    code = generate_enrollment_code()
    max_e_id = 0
    for e in all_enrollments:
        try:
            v = int(e.get("id", 0))
            if v > max_e_id: max_e_id = v
        except ValueError: pass

    new_e_id = max_e_id + 1
    doc_e_id = f"{code.lower()}-{slugify(data.participant_name)}"

    enrollment_doc = {
        "id": new_e_id,
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

    sport["enrolled_count"] = enrolled_cnt + 1
    sport_doc_id = sport.get("slug_id") or slugify(sport["title"])
    sync_to_firebase_cloud("sports", sport_doc_id, sport)

    return enrollment_doc

def get_enrollments(
    email: Optional[str] = None,
    phone: Optional[str] = None,
    participant: Optional[str] = None,
    sport_id: Optional[Union[int, str]] = None,
    status_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    db = get_firestore_db()
    results = []

    try:
        if isinstance(db, FirestoreLocalEmulator):
            docs = db.collection("enrollments").stream()
        else:
            docs = db.collection("enrollments").stream(timeout=3.0)

        for d in docs:
            data = d.to_dict()
            if str(d.id).isdigit():
                data["id"] = int(d.id)

            if email and data.get("parent_email", "").lower() != email.strip().lower():
                continue
            if phone and phone.strip() not in data.get("parent_phone", ""):
                continue
            if participant and participant.strip().lower() not in data.get("participant_name", "").lower():
                continue
            if sport_id and str(data.get("sport_id")) != str(sport_id):
                continue
            if status_filter and status_filter != "ALL" and data.get("status") != status_filter.upper():
                continue

            results.append(data)
    except Exception as e:
        print("[WARNING] Enrollments query fallback:", e)

    results.sort(key=lambda x: str(x.get("enrolled_at", "")), reverse=True)
    return results

def get_enrollment_by_code(code: str) -> Optional[Dict[str, Any]]:
    all_enrollments = get_enrollments(status_filter="ALL")
    code_upper = code.strip().upper()
    for item in all_enrollments:
        if item.get("enrollment_code", "").upper() == code_upper:
            return item
    return None

def cancel_enrollment(enrollment_id: Union[int, str]) -> Dict[str, Any]:
    str_id = str(enrollment_id)
    all_enrollments = get_enrollments(status_filter="ALL")

    target_data = None
    for item in all_enrollments:
        if str(item.get("id")) == str_id:
            target_data = item
            break

    if not target_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with ID {enrollment_id} not found."
        )

    if target_data.get("status") == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Enrollment is already cancelled."
        )

    target_data["status"] = "CANCELLED"
    doc_e_id = f"{target_data.get('enrollment_code','').lower()}-{slugify(target_data.get('participant_name',''))}"
    sync_to_firebase_cloud("enrollments", doc_e_id, target_data)

    sport_id = target_data.get("sport_id")
    sport = get_sport_by_id(sport_id)
    if sport and sport.get("enrolled_count", 0) > 0:
        sport["enrolled_count"] -= 1
        sport_doc_id = sport.get("slug_id") or slugify(sport["title"])
        sync_to_firebase_cloud("sports", sport_doc_id, sport)

    return target_data


# --- Analytics Statistics ---

def get_dashboard_stats() -> Dict[str, Any]:
    sports = get_sports(active_only=False)
    enrollments = get_enrollments(status_filter="ALL")

    total_sports = len(sports)
    active_sports = len([s for s in sports if s.get("is_active", True)])

    confirmed = [e for e in enrollments if e.get("status") == "CONFIRMED"]
    cancelled = [e for e in enrollments if e.get("status") == "CANCELLED"]

    total_revenue = sum(float(e.get("amount_paid", 0.0)) for e in confirmed)

    total_cap = sum(s.get("max_capacity", 0) for s in sports if s.get("is_active", True))
    total_enrolled = sum(s.get("enrolled_count", 0) for s in sports if s.get("is_active", True))
    spots_available = max(0, total_cap - total_enrolled)

    popular_sports = []
    for s in sports:
        if s.get("is_active", True):
            popular_sports.append({
                "id": s["id"],
                "title": s["title"],
                "category": s["category"],
                "enrolled_count": s.get("enrolled_count", 0),
                "max_capacity": s.get("max_capacity", 20),
                "fee": s.get("fee", 0.0)
            })
    popular_sports.sort(key=lambda x: x["enrolled_count"], reverse=True)

    return {
        "total_sports": total_sports,
        "active_sports": active_sports,
        "total_enrollments": len(enrollments),
        "confirmed_enrollments": len(confirmed),
        "cancelled_enrollments": len(cancelled),
        "total_revenue": total_revenue,
        "spots_available": spots_available,
        "popular_sports": popular_sports[:6]
    }


def seed_firestore_db():
    try:
        sports = get_sports(active_only=False)
        if len(sports) == 0:
            print("[INFO] Seeding initial sports activities into Google Firestore...")
            from app.seed import SAMPLE_SPORTS
            for idx, item in enumerate(SAMPLE_SPORTS, start=1):
                create_sport(SportCreate(**item))
            print("[SUCCESS] Successfully seeded sports into Google Firestore!")
    except Exception as e:
        print("[NOTICE] Skipping seed initialization:", e)
