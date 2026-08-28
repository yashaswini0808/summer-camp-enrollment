import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("PURGING NUMERIC DOCUMENT IDs FROM FIREBASE")
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

print("--- Purging Numeric Sports Document IDs ('1' to '50') ---")
for i in range(1, 50):
    num_str = str(i)
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{num_str}"
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        print(f"[PURGED] Deleted numeric sport Document ID '{num_str}' from Firebase!")

print("\n--- Purging Numeric Enrollments Document IDs ('1' to '50') ---")
for i in range(1, 50):
    num_str = str(i)
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/enrollments/{num_str}"
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        print(f"[PURGED] Deleted numeric enrollment Document ID '{num_str}' from Firebase!")

print("\n==========================================")
print("SUCCESS! ALL NUMERIC DOCUMENTS PURGED FROM FIREBASE!")
print("==========================================")
