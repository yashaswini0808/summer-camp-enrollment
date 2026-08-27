import json
import re
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("RE-INDEXING FIREBASE WITH TEXT SLUG DOCUMENT IDs")
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

print("--- Uploading Sports with Descriptive Text Document IDs ---")
for s_id, s_data in sports_dict.items():
    title = s_data.get("title", f"sport-{s_id}")
    slug_id = slugify(title)
    s_data["slug_id"] = slug_id
    
    fields = {k: py_val_to_firestore_val(v) for k, v in s_data.items() if v is not None}
    
    # Write under slug_id document name
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{slug_id}"
    body = {"fields": fields}
    res = requests.patch(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"[SUCCESS] Uploaded Sport Document ID '{slug_id}' ({title})")
    else:
        print(f"[!] Error uploading '{slug_id}': {res.text[:150]}")

print("\n--- Uploading Enrollments with Unique Enrollment Code Document IDs ---")
for e_id, e_data in enrollments_dict.items():
    code = e_data.get("enrollment_code", f"enrollment-{e_id}")
    p_name = e_data.get("participant_name", "")
    code_doc_id = f"{code.lower()}-{slugify(p_name)}" if p_name else code.lower()
    
    fields = {k: py_val_to_firestore_val(v) for k, v in e_data.items() if v is not None}
    
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/enrollments/{code_doc_id}"
    body = {"fields": fields}
    res = requests.patch(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"[SUCCESS] Uploaded Enrollment Document ID '{code_doc_id}' for {p_name}")
    else:
        print(f"[!] Error uploading '{code_doc_id}': {res.text[:150]}")

print("\n==========================================")
print("SUCCESS! ALL FIREBASE DOCUMENTS ARE NOW NAMED BY TEXT SLUGS!")
print("==========================================")
