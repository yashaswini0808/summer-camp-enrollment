import os
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

# Try importing official Google Cloud Firestore / Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIRESTORE_SDK_AVAILABLE = True
except ImportError:
    FIRESTORE_SDK_AVAILABLE = False

class FirestoreLocalEmulator:
    """
    Local JSON-persisted Firestore emulator fallback.
    Used when live Google Firestore credentials are not configured in environment,
    allowing the application to execute out-of-the-box seamlessly.
    """
    def __init__(self, storage_file="firestore_local_db.json"):
        self.storage_file = storage_file
        self.data: Dict[str, Dict[str, Dict[str, Any]]] = {"sports": {}, "enrollments": {}}
        self.load()

    def load(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"sports": {}, "enrollments": {}}

    def save(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            print("Failed to persist local firestore emulator data:", e)

    def collection(self, col_name: str):
        if col_name not in self.data:
            self.data[col_name] = {}
        return DocumentQueryProxy(self, col_name)


class DocumentProxy:
    def __init__(self, emulator: FirestoreLocalEmulator, col_name: str, doc_id: str):
        self.emulator = emulator
        self.col_name = col_name
        self.id = str(doc_id)

    def get(self):
        col = self.emulator.data.get(self.col_name, {})
        data = col.get(self.id)
        return DocumentSnapshotProxy(self.id, data)

    def set(self, data: Dict[str, Any], merge: bool = False):
        if self.col_name not in self.emulator.data:
            self.emulator.data[self.col_name] = {}
        if merge and self.id in self.emulator.data[self.col_name]:
            self.emulator.data[self.col_name][self.id].update(data)
        else:
            self.emulator.data[self.col_name][self.id] = data
        self.emulator.save()

    def update(self, data: Dict[str, Any]):
        if self.col_name in self.emulator.data and self.id in self.emulator.data[self.col_name]:
            self.emulator.data[self.col_name][self.id].update(data)
            self.emulator.save()

    def delete(self):
        if self.col_name in self.emulator.data and self.id in self.emulator.data[self.col_name]:
            del self.emulator.data[self.col_name][self.id]
            self.emulator.save()


class DocumentSnapshotProxy:
    def __init__(self, doc_id: str, data: Optional[Dict[str, Any]]):
        self.id = doc_id
        self._data = data

    @property
    def exists(self):
        return self._data is not None

    def to_dict(self):
        return dict(self._data) if self._data else {}


class DocumentQueryProxy:
    def __init__(self, emulator: FirestoreLocalEmulator, col_name: str):
        self.emulator = emulator
        self.col_name = col_name

    def document(self, doc_id: Optional[str] = None):
        if not doc_id:
            doc_id = str(uuid.uuid4())
        return DocumentProxy(self.emulator, self.col_name, doc_id)

    def add(self, data: Dict[str, Any]):
        doc_id = str(len(self.emulator.data.get(self.col_name, {})) + 1)
        if "id" in data and data["id"]:
            doc_id = str(data["id"])
        doc = DocumentProxy(self.emulator, self.col_name, doc_id)
        data["id"] = int(doc_id) if doc_id.isdigit() else doc_id
        doc.set(data)
        return None, doc

    def stream(self):
        col = self.emulator.data.get(self.col_name, {})
        snapshots = []
        for doc_id, data in col.items():
            snapshots.append(DocumentSnapshotProxy(doc_id, data))
        return snapshots

    def get(self):
        return self.stream()


# --- Firestore Initialization Logic ---

db_client = None
USE_LIVE_FIRESTORE = False

# Search for credentials in env vars or local file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_json = os.path.join(base_dir, "firebase_credentials.json")

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path and os.path.exists(default_json):
    cred_path = default_json

if FIRESTORE_SDK_AVAILABLE and cred_path and os.path.exists(cred_path):
    try:
        cred = credentials.Certificate(cred_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db_client = firestore.client(database="default")
        # Test query to verify database default exists
        db_client.collection("sports").limit(1).get(timeout=3.0)
        USE_LIVE_FIRESTORE = True
        print(f"[SUCCESS] Connected to Live Google Firestore using credentials: {cred_path}")
    except Exception as e:
        print(f"[WARNING] Live Firestore Cloud Database not ready or pending setup in Console ({e}). Using local persistent database.")
        db_client = FirestoreLocalEmulator()

else:
    print("[INFO] Running Google Firestore Client in Local Persistent Emulator Mode.")
    db_client = FirestoreLocalEmulator()




def get_firestore_db():
    """Returns the initialized Firestore client (Live or Emulator)"""
    return db_client
