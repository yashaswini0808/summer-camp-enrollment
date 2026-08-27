import os
from google.cloud import firestore
from google.oauth2 import service_account

credentials_path = "firebase_credentials.json"
creds = service_account.Credentials.from_service_account_file(credentials_path)

for db_name in ["(default)", "summer-camp-app-ec377"]:
    try:
        print(f"Testing direct google.cloud.firestore Client with database='{db_name}'...")
        client = firestore.Client(project="summer-camp-app-ec377", credentials=creds, database=db_name)
        client.collection("sports").document("99").set({"title": "Direct Test"})
        print(f"SUCCESS on database '{db_name}'!")
    except Exception as e:
        print(f"Error on '{db_name}': {e}")
