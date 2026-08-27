import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_credentials.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

try:
    db = firestore.client()
    print("Testing default database...")
    docs = list(db.collection("sports").stream())
    print("SUCCESS on default database! Docs:", len(docs))
except Exception as e:
    print("Error on default database:", e)
