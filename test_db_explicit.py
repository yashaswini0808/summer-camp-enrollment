import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_credentials.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

for db_name in ["(default)", "summer-camp-app-ec377"]:
    try:
        print(f"Testing database: {db_name}...")
        db = firestore.client(database=db_name)
        db.collection("test").document("1").set({"status": "ok"})
        print(f"SUCCESS on database '{db_name}'!")
    except Exception as e:
        print(f"Error on '{db_name}': {e}")
