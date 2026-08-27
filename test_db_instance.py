import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_credentials.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

try:
    # Try default client
    db = firestore.client()
    print("Testing default Firestore client...")
    doc_ref = db.collection("sports").document("1")
    doc_ref.set({"test": "ok"})
    print("SUCCESS: Default database connected!")
except Exception as e:
    print("Default db error:", e)
