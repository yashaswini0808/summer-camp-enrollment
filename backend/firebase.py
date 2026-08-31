import os
import json
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "summer-camp-app-ec377")

_db_client = None

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK securely using environment variables or service account configuration.
    Flow: FastAPI -> firebase.py -> Firebase Admin SDK -> Firestore
    """
    global _db_client
    if _db_client is not None:
        return _db_client

    print("[FIREBASE] Initializing Firebase Admin SDK...")
    
    # 1. Check for service account file path
    cred_file = Path(__file__).resolve().parent / FIREBASE_CREDENTIALS_PATH
    if not cred_file.exists():
        cred_file = Path(FIREBASE_CREDENTIALS_PATH)

    if cred_file.exists():
        try:
            cred = credentials.Certificate(str(cred_file))
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred, {
                    'projectId': FIREBASE_PROJECT_ID,
                })
            _db_client = firestore.client()
            print(f"[FIREBASE SUCCESS] Connected to Firestore project '{FIREBASE_PROJECT_ID}' via Certificate.")
            return _db_client
        except Exception as e:
            print(f"[FIREBASE WARNING] Certificate init notice: {e}")

    # 2. Fallback to default application credentials or environment variable JSON string
    try:
        env_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if env_json:
            cred_dict = json.loads(env_json)
            cred = credentials.Certificate(cred_dict)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            _db_client = firestore.client()
            print(f"[FIREBASE SUCCESS] Connected to Firestore via FIREBASE_CREDENTIALS_JSON env var.")
            return _db_client
    except Exception as e:
        print(f"[FIREBASE WARNING] Env JSON init notice: {e}")

    # 3. Fallback to default firebase initialization
    try:
        if not firebase_admin._apps:
            firebase_admin.initialize_app()
        _db_client = firestore.client()
        print("[FIREBASE SUCCESS] Connected via default credentials.")
        return _db_client
    except Exception as e:
        print(f"[FIREBASE NOTICE] Standard SDK fallback mode: {e}")
        return None

def get_db():
    """Returns the initialized Firestore database client instance."""
    global _db_client
    if _db_client is None:
        _db_client = initialize_firebase()
    return _db_client
