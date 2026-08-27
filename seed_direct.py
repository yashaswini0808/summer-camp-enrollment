import time
import firebase_admin
from firebase_admin import credentials, firestore
from app.seed import SAMPLE_SPORTS

cred = credentials.Certificate("firebase_credentials.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("Attempting direct document upload to Firebase...")
for idx, item in enumerate(SAMPLE_SPORTS, start=1):
    try:
        data = dict(item)
        data["id"] = idx
        data["enrolled_count"] = 0
        data["is_active"] = True
        db.collection("sports").document(str(idx)).set(data)
        print(f"Uploaded Sport #{idx}: {item['title']}")
    except Exception as e:
        print(f"Error uploading #{idx}: {e}")

print("Done direct seed check!")
