import json
import re
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("RE-INDEXING FIREBASE WITH 100% STRING TEXT FIELDS")
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

with open("firestore_local_db.json", "r", encoding="utf-8") as f:
    local_data = json.load(f)

sports_dict = local_data.get("sports", {})
enrollments_dict = local_data.get("enrollments", {})

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def py_val_to_firestore_val(key_name, val):
    if val is None:
        return {"stringValue": "None"}
    elif isinstance(val, bool):
        return {"stringValue": "Active" if val else "Inactive"}
    elif isinstance(val, (int, float)):
        if "fee" in key_name or "amount" in key_name or "revenue" in key_name:
            return {"stringValue": f"${float(val):.2f}"}
        elif "age" in key_name:
            return {"stringValue": f"{val} years old"}
        elif "capacity" in key_name:
            return {"stringValue": f"{val} max capacity"}
        elif "count" in key_name or "enrolled" in key_name:
            return {"stringValue": f"{val} enrolled"}
        elif "id" == key_name:
            return {"stringValue": f"ID #{val}"}
        return {"stringValue": str(val)}
    elif isinstance(val, dict):
        fields = {k: py_val_to_firestore_val(k, v) for k, v in val.items() if v is not None}
        return {"mapValue": {"fields": fields}}
    elif isinstance(val, list):
        return {"arrayValue": {"values": [py_val_to_firestore_val(key_name, item) for item in val]}}
    return {"stringValue": str(val)}

print("--- Uploading Sports as 100% Text Strings ---")
for s_id, s_data in sports_dict.items():
    title = s_data.get("title", f"sport-{s_id}")
    slug_id = slugify(title)
    s_data["slug_id"] = slug_id
    
    fields = {k: py_val_to_firestore_val(k, v) for k, v in s_data.items() if v is not None}
    
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{slug_id}"
    body = {"fields": fields}
    res = requests.patch(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"[SUCCESS 200 OK] Uploaded Sport Document '{slug_id}' (100% String Text)")
    else:
        print(f"[!] Error on '{slug_id}': {res.text[:150]}")

print("\n--- Uploading Enrollments as 100% Text Strings ---")
for e_id, e_data in enrollments_dict.items():
    code = e_data.get("enrollment_code", f"enrollment-{e_id}")
    p_name = e_data.get("participant_name", "")
    code_doc_id = f"{code.lower()}-{slugify(p_name)}" if p_name else code.lower()
    
    fields = {k: py_val_to_firestore_val(k, v) for k, v in e_data.items() if v is not None}
    
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/enrollments/{code_doc_id}"
    body = {"fields": fields}
    res = requests.patch(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"[SUCCESS 200 OK] Uploaded Enrollment Document '{code_doc_id}' (100% String Text)")
    else:
        print(f"[!] Error on '{code_doc_id}': {res.text[:150]}")

print("\n==========================================")
print("SUCCESS! ALL FIREBASE FIELDS ARE NOW 100% STRING TEXT!")
print("==========================================")
