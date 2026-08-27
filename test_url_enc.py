import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

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

body = {"fields": {"title": {"stringValue": "Junior Soccer Champions"}}}

for db_str in ["(default)", "%28default%29", "default"]:
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/{db_str}/documents/sports/1"
    res = requests.patch(url, headers=headers, json=body)
    print(f"Testing REST db parameter '{db_str}': Status {res.status_code}")
    if res.status_code == 200:
        print("SUCCESS Output:", res.json().get("name"))
    else:
        print("Error snippet:", res.text[:200])
