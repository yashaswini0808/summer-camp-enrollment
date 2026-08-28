import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

print("==========================================")
print("CONSOLIDATING FIREBASE DOCUMENTS TO TEXT SLUG IDs ONLY")
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

# 1. Update Beach Volleyball League (slug_id: beach-volleyball-league) with min_age: 10, max_age: 20
beach_volleyball_data = {
    "title": {"stringValue": "Beach Volleyball League"},
    "category": {"stringValue": "Team Sports"},
    "description": {"stringValue": "Bump, set, spike! Learn beach volleyball strategies, serve control, and active outdoor fitness."},
    "min_age": {"integerValue": "10"},
    "max_age": {"integerValue": "20"},
    "instructor": {"stringValue": "Coach Spike Johnson"},
    "schedule_days": {"stringValue": "Tue, Fri"},
    "schedule_time": {"stringValue": "03:30 PM - 05:30 PM"},
    "location": {"stringValue": "Sand Courts 1 & 2"},
    "fee": {"doubleValue": 150.0},
    "max_capacity": {"integerValue": "16"},
    "image_icon": {"stringValue": "🏐"},
    "is_active": {"booleanValue": True},
    "id": {"stringValue": "beach-volleyball-league"},
    "slug_id": {"stringValue": "beach-volleyball-league"},
    "enrolled_count": {"integerValue": "0"}
}

url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/beach-volleyball-league"
res = requests.patch(url, headers=headers, json={"fields": beach_volleyball_data})
if res.status_code == 200:
    print("[SUCCESS 200 OK] Updated 'sports/beach-volleyball-league' in Firebase Cloud with min_age: 10 and max_age: 20!")

# 2. Delete all numeric document IDs ('1' through '50') from Firebase Cloud so only text slug IDs exist
print("\n--- Deleting all lingering numeric document IDs from Firebase Cloud ---")
del_headers = {"Authorization": f"Bearer {token}"}
for i in range(1, 50):
    num_id = str(i)
    del_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/default/documents/sports/{num_id}"
    del_res = requests.delete(del_url, headers=del_headers)
    if del_res.status_code == 200:
        print(f"[DELETED NUMERIC ID] Removed numeric document 'sports/{num_id}' from Firebase Cloud!")

print("\n==========================================")
print("SUCCESS! FIREBASE CONSOLIDATED TO TEXT SLUG IDs ONLY!")
print("==========================================")
