import firebase_admin
from firebase_admin import credentials, firestore

print("Attempting admin document creation via Firebase Admin SDK...")
cred = credentials.Certificate("firebase_credentials.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

try:
    db = firestore.client()
    doc_ref = db.collection("sports").document("1")
    doc_ref.set({
        "id": 1,
        "title": "Junior Soccer Academy",
        "category": "Team Sports",
        "description": "Comprehensive soccer training focusing on footwork and team matches.",
        "min_age": 6,
        "max_age": 12,
        "instructor": "Coach Alex Morgan",
        "schedule_days": "Mon, Wed, Fri",
        "schedule_time": "09:00 AM - 11:00 AM",
        "location": "Main Turf Pitch A",
        "fee": 160.0,
        "max_capacity": 20,
        "enrolled_count": 0,
        "image_icon": "⚽",
        "is_active": True
    })
    print("SUCCESS! Document created via Admin SDK!")
except Exception as e:
    print("Admin SDK error:", e)
