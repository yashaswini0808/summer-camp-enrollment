import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("CHECKING FIREBASE CLOUD DOCUMENTS FOR BEACH VOLLEYBALL")
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

headers = {"Authorization": f"Bearer {token}"}

url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports"
res = requests.get(url, headers=headers)

if res.status_code == 200:
    docs = res.json().get("documents", [])
    print(f"Total sports documents in Firebase Cloud: {len(docs)}\n")
    for doc in docs:
        doc_id = doc["name"].split("/")[-1]
        fields = doc.get("fields", {})
        title = fields.get("title", {}).get("stringValue", "N/A")
        min_a = fields.get("min_age", {}).get("integerValue", fields.get("min_age", {}).get("stringValue", "N/A"))
        max_a = fields.get("max_age", {}).get("integerValue", fields.get("max_age", {}).get("stringValue", "N/A"))
        print(f"Doc ID: '{doc_id}' | Title: '{title}' | min_age: {min_a} | max_age: {max_a}")

print("==========================================")
