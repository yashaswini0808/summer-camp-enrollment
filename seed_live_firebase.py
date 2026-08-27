import os
import firebase_admin
from firebase_admin import credentials, firestore
from app.seed import SAMPLE_SPORTS

print("==========================================")
print("SEEDING LIVE GOOGLE CLOUD FIRESTORE")
print("==========================================")

cred_file = "firebase_credentials.json"
cred = credentials.Certificate(cred_file)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

sports_col = db.collection("sports")
existing_docs = list(sports_col.stream())

print(f"Existing sports documents in Firebase: {len(existing_docs)}")

if len(existing_docs) == 0:
    print("Uploading 8 sample sports activities to your live Firebase project...")
    for idx, item in enumerate(SAMPLE_SPORTS, start=1):
        item_copy = dict(item)
        item_copy["id"] = idx
        item_copy["enrolled_count"] = 0
        item_copy["is_active"] = True
        sports_col.document(str(idx)).set(item_copy)
    print("SUCCESS! All sports successfully created in your live Firebase Firestore Database!")
else:
    print("Sports collection already contains data in Firebase!")

print("==========================================")
