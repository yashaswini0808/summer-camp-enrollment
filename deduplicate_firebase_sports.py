import json
import re
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("CLEANING UP DUPLICATE SPORTS IN FIREBASE CONSOLE")
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
    "Authorization": f"Bearer {token}"
}

# 1. Fetch current sports documents from Firebase Cloud REST API
url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports"
res = requests.get(url, headers=headers)

if res.status_code == 200:
    docs = res.json().get("documents", [])
    print(f"Found {len(docs)} documents in 'sports' collection.")
    
    seen_titles = {}
    for doc in docs:
        doc_name = doc["name"].split("/")[-1]
        fields = doc.get("fields", {})
        title_val = fields.get("title", {}).get("stringValue", doc_name)
        
        if title_val in seen_titles:
            # Delete duplicate document
            del_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{doc_name}"
            del_res = requests.delete(del_url, headers=headers)
            if del_res.status_code == 200:
                print(f"[DELETED DUPLICATE] Removed duplicate document ID '{doc_name}' for title '{title_val}'")
        else:
            seen_titles[title_val] = doc_name

print("\n==========================================")
print("SUCCESS! DUPLICATE DOCUMENTS REMOVED FROM FIREBASE CONSOLE!")
print("==========================================")
