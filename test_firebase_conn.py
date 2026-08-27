import os
import firebase_admin
from firebase_admin import credentials, firestore

print("==========================================")
print("FIREBASE CONNECTION TEST DIAGNOSTIC")
print("==========================================")

cred_file = "firebase_credentials.json"

if not os.path.exists(cred_file):
    print(f"[!] '{cred_file}' NOT FOUND in current folder.")
    print("Please place 'firebase_credentials.json' inside this directory.")
else:
    print(f"[+] Found '{cred_file}'. Connecting to Google Cloud Firestore...")
    try:
        cred = credentials.Certificate(cred_file)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        
        # Test read query
        docs = list(db.collection("sports").stream())
        print("SUCCESS! Connected to Live Google Firebase Firestore Database!")
        print(f"Current documents in 'sports' collection: {len(docs)}")
    except Exception as e:
        print(f"[!] Connection error: {e}")

print("==========================================")
