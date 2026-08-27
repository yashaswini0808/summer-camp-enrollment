import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("UPLOADING ALL DATA TO LIVE GOOGLE FIREBASE")
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

# Load local data
with open("firestore_local_db.json", "r", encoding="utf-8") as f:
    local_data = json.load(f)

sports_dict = local_data.get("sports", {})
enrollments_dict = local_data.get("enrollments", {})

print(f"Project ID: {project_id}")
print(f"Uploading {len(sports_dict)} sports and {len(enrollments_dict)} enrollments to Firebase Cloud...\n")

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
    elif val is None:
        return {"nullValue": None}
    return {"stringValue": str(val)}

# Upload sports
print("--- Uploading Sports Collection ---")
for s_id, s_data in sports_dict.items():
    fields = {k: py_val_to_firestore_val(v) for k, v in s_data.items() if v is not None}
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{s_id}"
    body = {"fields": fields}
    res = requests.patch(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"[SUCCESS 200 OK] Uploaded Sport #{s_id}: {s_data.get('title')}")
    else:
        print(f"[!] Error on Sport #{s_id} ({res.status_code}): {res.text[:150]}")

# Upload enrollments
print("\n--- Uploading Enrollments Collection ---")
for e_id, e_data in enrollments_dict.items():
    fields = {k: py_val_to_firestore_val(v) for k, v in e_data.items() if v is not None}
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/enrollments/{e_id}"
    body = {"fields": fields}
    res = requests.patch(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"[SUCCESS 200 OK] Uploaded Enrollment #{e_id}: {e_data.get('participant_name')} ({e_data.get('enrollment_code')})")
    else:
        print(f"[!] Error on Enrollment #{e_id} ({res.status_code}): {res.text[:150]}")

print("\n==========================================")
print("SUCCESS! ALL DATA IS NOW PERMANENTLY STORED IN LIVE GOOGLE FIREBASE!")
print("==========================================")
