import json
import re
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("SEEDING ALL 6 NEW COLLECTIONS TO GOOGLE FIREBASE")
print("==========================================")

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

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def py_val_to_firestore_val(val):
    if isinstance(val, bool):
        return {"booleanValue": val}
    elif isinstance(val, int):
        return {"integerValue": str(val)}
    elif isinstance(val, float):
        return {"doubleValue": val}
    elif isinstance(val, str):
        return {"stringValue": val}
    elif isinstance(val, dict):
        fields = {k: py_val_to_firestore_val(v) for k, v in val.items() if v is not None}
        return {"mapValue": {"fields": fields}}
    elif isinstance(val, list):
        return {"arrayValue": {"values": [py_val_to_firestore_val(item) for item in val]}}
    elif val is None:
        return {"nullValue": None}
    return {"stringValue": str(val)}

def upload_collection(collection_name, data_list, id_key):
    print(f"\n--- Uploading '{collection_name}' Collection ({len(data_list)} items) ---")
    for item in data_list:
        doc_id = slugify(str(item.get(id_key)))
        fields = {k: py_val_to_firestore_val(v) for k, v in item.items() if v is not None}
        url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/{collection_name}/{doc_id}"
        body = {"fields": fields}
        res = requests.patch(url, headers=headers, json=body)
        if res.status_code == 200:
            print(f"[SUCCESS 200 OK] Uploaded {collection_name}/{doc_id}")
        else:
            print(f"[!] Error on {collection_name}/{doc_id}: {res.text[:150]}")

# 1. COACHES
coaches = [
    {
        "name": "Coach Alex Morgan",
        "specialization": "Team Sports & Soccer",
        "experience_years": 8,
        "email": "alex.morgan@summercamp.org",
        "phone": "+1-555-0144",
        "bio": "Former collegiate soccer captain certified in youth sports coaching and tactical training.",
        "rating": 4.9,
        "is_active": True
    },
    {
        "name": "Coach Marcus Vance",
        "specialization": "Basketball & Conditioning",
        "experience_years": 10,
        "email": "marcus.vance@summercamp.org",
        "phone": "+1-555-0188",
        "bio": "Specializes in high-energy dribbling drills, jump shooting, and court teamwork.",
        "rating": 4.8,
        "is_active": True
    },
    {
        "name": "Coach Elena Rostova",
        "specialization": "Water Sports & Swimming",
        "experience_years": 12,
        "email": "elena.rostova@summercamp.org",
        "phone": "+1-555-0211",
        "bio": "Certified lifeguard instructor and stroke technique specialist for all skill levels.",
        "rating": 5.0,
        "is_active": True
    },
    {
        "name": "Coach David Miller",
        "specialization": "Racket Sports & Tennis",
        "experience_years": 7,
        "email": "david.miller@summercamp.org",
        "phone": "+1-555-0344",
        "bio": "Pro tennis circuit veteran passionate about junior footwork and match play.",
        "rating": 4.7,
        "is_active": True
    }
]

# 2. LOCATIONS
locations = [
    {
        "name": "Main Turf Pitch A",
        "type": "Outdoor Grass Pitch",
        "capacity": 100,
        "features": ["Sub-surface Drainage", "Floodlights", "Padded Goal Posts"],
        "address": "Zone 1 - North Sports Complex"
    },
    {
        "name": "Indoor Arena Court 1",
        "type": "Hardwood Court",
        "capacity": 150,
        "features": ["Air Conditioned", "Maple Flooring", "Glass Backboards"],
        "address": "Zone 2 - Central Recreation Center"
    },
    {
        "name": "Olympic Heated Pool",
        "type": "Aquatic Center",
        "capacity": 80,
        "features": ["Heated Water", "Diving Platforms", "Lifeguard Station"],
        "address": "Zone 3 - West Aquatic Pavilion"
    },
    {
        "name": "Hard Courts 3 & 4",
        "type": "Outdoor Tennis Courts",
        "capacity": 40,
        "features": ["Acrylic Coating", "Shade Canopies", "Automatic Ball Machines"],
        "address": "Zone 4 - East Tennis Grounds"
    }
]

# 3. PAYMENTS
payments = [
    {
        "invoice_id": "INV-2026-001",
        "enrollment_code": "CAMP-2026-4FN85",
        "parent_name": "Savitri",
        "amount": 160.0,
        "payment_method": "Credit Card",
        "status": "PAID",
        "transaction_date": "2026-08-26T11:33:26Z"
    },
    {
        "invoice_id": "INV-2026-002",
        "enrollment_code": "CAMP-2026-ZW7OD",
        "parent_name": "Sa",
        "amount": 200.0,
        "payment_method": "2-Installments Plan",
        "status": "PARTIAL",
        "transaction_date": "2026-08-26T11:38:47Z"
    },
    {
        "invoice_id": "INV-2026-003",
        "enrollment_code": "CAMP-2026-X7MBU",
        "parent_name": "Nisha",
        "amount": 200.0,
        "payment_method": "Debit Card",
        "status": "PAID",
        "transaction_date": "2026-08-27T06:48:26Z"
    }
]

# 4. USERS (PARENTS)
users = [
    {
        "parent_name": "Savitri",
        "email": "divyashreens11@gmail.com",
        "phone": "+919449490392",
        "children": ["Yashaswini M V"],
        "account_type": "Parent",
        "member_since": "2026-08-26"
    },
    {
        "parent_name": "Nisha",
        "email": "kerthi12@gmail.com",
        "phone": "321846549",
        "children": ["nisarga"],
        "account_type": "Parent",
        "member_since": "2026-08-27"
    },
    {
        "parent_name": "Admin Manager",
        "email": "admin@summercamp.org",
        "phone": "+1-555-0000",
        "children": [],
        "account_type": "Administrator",
        "member_since": "2026-01-01"
    }
]

# 5. REVIEWS
reviews = [
    {
        "review_id": "REV-001",
        "sport_title": "AquaSplash Swimming & Water Safety",
        "reviewer_name": "Nisha",
        "rating": 5,
        "comment": "My daughter nisarga loved the instructors! Super safe and great water skills.",
        "created_at": "2026-08-27T07:10:00Z"
    },
    {
        "review_id": "REV-002",
        "sport_title": "Junior Soccer Champions",
        "reviewer_name": "Savitri",
        "rating": 5,
        "comment": "Yashaswini had an amazing time on Pitch A with Coach Alex. High energy drills!",
        "created_at": "2026-08-26T12:00:00Z"
    }
]

# 6. ATTENDANCE
attendance = [
    {
        "attendance_id": "ATT-2026-08-26-01",
        "date": "2026-08-26",
        "sport_title": "Junior Soccer Champions",
        "student_name": "Yashaswini M V",
        "status": "PRESENT",
        "checkin_time": "08:55 AM",
        "notes": "Arrived on time in full uniform."
    },
    {
        "attendance_id": "ATT-2026-08-27-01",
        "date": "2026-08-27",
        "sport_title": "AquaSplash Swimming & Water Safety",
        "student_name": "nisarga",
        "status": "PRESENT",
        "checkin_time": "08:25 AM",
        "notes": "Completed 5 lap swimming drill."
    }
]

upload_collection("coaches", coaches, "name")
upload_collection("locations", locations, "name")
upload_collection("payments", payments, "invoice_id")
upload_collection("users", users, "parent_name")
upload_collection("reviews", reviews, "review_id")
upload_collection("attendance", attendance, "attendance_id")

print("\n==========================================")
print("SUCCESS! ALL 6 NEW COLLECTIONS ARE LIVE IN FIREBASE CONSOLE!")
print("==========================================")
