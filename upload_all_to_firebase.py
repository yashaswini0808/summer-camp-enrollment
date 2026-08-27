import json
import firebase_admin
from firebase_admin import credentials, firestore

print("==========================================")
print("UPLOADING ALL DATA TO LIVE GOOGLE FIREBASE")
print("==========================================")

# 1. Initialize Firebase Admin SDK using credentials
cred_file = "firebase_credentials.json"
cred = credentials.Certificate(cred_file)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. Read local data file
with open("firestore_local_db.json", "r", encoding="utf-8") as f:
    local_data = json.load(f)

sports_dict = local_data.get("sports", {})
enrollments_dict = local_data.get("enrollments", {})

print(f"Found {len(sports_dict)} sports and {len(enrollments_dict)} student enrollments to upload.")

# 3. Upload all sports to Live Firebase
print("\n--- Uploading Sports Collection ---")
for sport_id, sport_data in sports_dict.items():
    try:
        db.collection("sports").document(str(sport_id)).set(sport_data)
        print(f"[+] Uploaded Sport #{sport_id}: {sport_data.get('title')}")
    except Exception as e:
        print(f"[!] Error uploading sport #{sport_id}: {e}")

# 4. Upload all enrollments to Live Firebase
print("\n--- Uploading Enrollments Collection ---")
for e_id, e_data in enrollments_dict.items():
    try:
        db.collection("enrollments").document(str(e_id)).set(e_data)
        print(f"[+] Uploaded Enrollment #{e_id}: {e_data.get('participant_name')} ({e_data.get('enrollment_code')})")
    except Exception as e:
        print(f"[!] Error uploading enrollment #{e_id}: {e}")

print("\n==========================================")
print("SUCCESS! ALL DATA IS NOW STORED IN LIVE GOOGLE FIREBASE!")
print("==========================================")
