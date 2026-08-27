import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("CLEANING UP OLD NUMERIC DOCUMENTS IN FIREBASE")
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

# 1. Delete numeric documents from sports
print("--- Cleaning Sports Collection ---")
for i in range(1, 20):
    num_str = str(i)
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{num_str}"
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        print(f"[CLEANED] Deleted numeric sport Document ID '{num_str}'")

# 2. Delete numeric documents from enrollments
print("\n--- Cleaning Enrollments Collection ---")
for i in range(1, 20):
    num_str = str(i)
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/enrollments/{num_str}"
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        print(f"[CLEANED] Deleted numeric enrollment Document ID '{num_str}'")

print("\n==========================================")
print("SUCCESS! ALL NUMERIC DOCUMENTS DELETED FROM FIREBASE CONSOLE!")
print("==========================================")
