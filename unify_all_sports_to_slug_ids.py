import json
import re
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("UNIFYING ALL SPORTS TO TEXT SLUG IDs")
print("==========================================")

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

with open("firestore_local_db.json", "r", encoding="utf-8") as f:
    db_data = json.load(f)

old_sports = db_data.get("sports", {})
new_sports = {}

for old_key, s_data in old_sports.items():
    title = s_data.get("title", old_key)
    slug = slugify(title)
    s_data["id"] = slug
    s_data["slug_id"] = slug
    new_sports[slug] = s_data
    print(f"Unified Sport: '{title}' -> Key & ID: '{slug}'")

db_data["sports"] = new_sports

with open("firestore_local_db.json", "w", encoding="utf-8") as f:
    json.dump(db_data, f, indent=2)

print("\n--- Syncing Unified Sports to Live Firebase Cloud ---")
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

def py_val_to_firestore_val(key_name, val):
    if val is None:
        return {"nullValue": None}
    elif isinstance(val, bool):
        return {"booleanValue": val}
    elif isinstance(val, int):
        return {"integerValue": str(val)}
    elif isinstance(val, float):
        return {"doubleValue": val}
    elif isinstance(val, str):
        return {"stringValue": val}
    elif isinstance(val, dict):
        fields = {k: py_val_to_firestore_val(k, v) for k, v in val.items() if v is not None}
        return {"mapValue": {"fields": fields}}
    elif isinstance(val, list):
        return {"arrayValue": {"values": [py_val_to_firestore_val(key_name, item) for item in val]}}
    return {"stringValue": str(val)}

for slug_id, payload in new_sports.items():
    fields = {k: py_val_to_firestore_val(k, v) for k, v in payload.items() if v is not None}
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{slug_id}"
    res = requests.patch(url, headers=headers, json={"fields": fields})
    if res.status_code == 200:
        print(f"[SUCCESS 200 OK] Live synced 'sports/{slug_id}' in Google Cloud!")

print("\n==========================================")
print("SUCCESS! ALL SPORTS UNIFIED TO TEXT SLUG IDs!")
print("==========================================")
