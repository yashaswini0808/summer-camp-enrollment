import google.auth
from google.auth.transport.requests import Request
import requests
import json

credentials_path = "firebase_credentials.json"
with open(credentials_path) as f:
    key_info = json.load(f)

project_id = key_info["project_id"]

from google.oauth2 import service_account
creds = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

creds.refresh(Request())
token = creds.token

print(f"Project ID: {project_id}")

# 1. List Firestore databases via REST API
url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases"
headers = {"Authorization": f"Bearer {token}"}

res = requests.get(url, headers=headers)
print("Firestore Databases REST Response Status:", res.status_code)
print("Response JSON:\n", json.dumps(res.json(), indent=2))
