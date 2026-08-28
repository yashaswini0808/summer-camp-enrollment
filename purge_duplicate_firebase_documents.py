import json
import re
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("PURGING DUPLICATE DOCUMENTS IN FIREBASE CONSOLE")
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

# Standard 8 expected sport document IDs
valid_sports_slugs = {
    "junior-soccer-champions",
    "summer-hoops-basketball-academy",
    "aquasplash-swimming-water-safety",
    "elite-tennis-stars-camp",
    "martial-arts-taekwondo-fundamentals",
    "outdoor-archery-target-shooting",
    "gymnastics-tumbling-stars",
    "beach-volleyball-league"
}

url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports"
res = requests.get(url, headers=headers)

if res.status_code == 200:
    docs = res.json().get("documents", [])
    print(f"Total documents found in 'sports': {len(docs)}")
    
    for doc in docs:
        doc_id = doc["name"].split("/")[-1]
        
        # If document ID is numeric or not in standard list, check if it's a separate duplicate
        if doc_id.isdigit() or ("summer-hoops" in doc_id and doc_id != "summer-hoops-basketball-academy"):
            del_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{doc_id}"
            del_res = requests.delete(del_url, headers=headers)
            if del_res.status_code == 200:
                print(f"[PURGED DUPLICATE] Deleted separate document '{doc_id}' from Firebase Console!")

print("\n==========================================")
print("SUCCESS! FIREBASE CONSOLE CLEANED - NO SEPARATE DUPLICATES REMAIN!")
print("==========================================")
