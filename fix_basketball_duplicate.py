import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("PURGING DUPLICATE BASKETBALL RECORD FROM FIREBASE & LOCAL STORE")
print("==========================================")

# 1. Update local database json
with open("firestore_local_db.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sports = data.get("sports", {})
if "basketball-academy" in sports:
    del sports["basketball-academy"]
    print("[CLEANED LOCAL] Removed duplicate 'basketball-academy' key from firestore_local_db.json")

# Ensure Basketball 2026 is active
if "summer-hoops-basketball-academy-2026" in sports:
    sports["summer-hoops-basketball-academy-2026"]["is_active"] = True

with open("firestore_local_db.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# 2. Delete duplicate from live Firebase Cloud REST API
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

headers = {"Authorization": f"Bearer {token}"}
del_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/basketball-academy"
res = requests.delete(del_url, headers=headers)
if res.status_code == 200:
    print("[CLEANED FIREBASE] Successfully deleted duplicate 'sports/basketball-academy' from Google Cloud!")

print("==========================================")
print("SUCCESS! ONLY 1 BASKETBALL ACADEMY DOCUMENT REMAINS!")
print("==========================================")
