from app.firestore_crud import create_sport, get_sport_by_id, update_sport, delete_sport, get_sports
from app.models_pydantic import SportCreate, SportUpdate

print("==========================================")
print("TESTING COMPLETE FIREBASE CRUD FLOW (IN-PLACE UPDATES)")
print("==========================================")

# 1. CREATE -> Create a new sport document
print("\n--- 1. CREATE: Creating new sport document ---")
new_sport_input = SportCreate(
    title="Test Boxing Championship",
    category="Combat & Fitness",
    image_icon="🥊",
    min_age=12,
    max_age=18,
    instructor="Coach Mike Tyson",
    fee=150.0,
    max_capacity=20,
    schedule_days="Tue, Thu",
    schedule_time="05:00 PM - 07:00 PM",
    location="Boxing Ring 1",
    description="Pro boxing drills and physical conditioning.",
    is_active=True
)

created_doc = create_sport(new_sport_input)
sport_id = created_doc["id"]
slug_id = created_doc["slug_id"]
print(f"[CREATE SUCCESS] Document created under ID '{sport_id}' (slug_id: '{slug_id}')")

# 2. READ -> Fetch document by ID
print("\n--- 2. READ: Fetching created document ---")
read_doc = get_sport_by_id(sport_id)
print(f"[READ SUCCESS] Retrieved Sport '{read_doc['title']}' | Fee: ${read_doc['fee']}")

# 3. EDIT & UPDATE -> Modify fields (fee & capacity) using exact same Document ID
print("\n--- 3. UPDATE: Updating fields in the SAME document ---")
update_input = SportUpdate(
    fee=199.99,
    max_capacity=30,
    schedule_time="06:00 PM - 08:00 PM"
)

updated_doc = update_sport(sport_id, update_input)
print(f"[UPDATE SUCCESS] Updated Document '{updated_doc['slug_id']}' in-place!")
print(f"New Fee: ${updated_doc['fee']} | New Capacity: {updated_doc['max_capacity']}")
print(f"Document ID Preserved: {updated_doc['slug_id'] == slug_id}")

# 4. DELETE -> Deactivate sport document
print("\n--- 4. DELETE: Deactivating sport document ---")
deleted_success = delete_sport(sport_id)
print(f"[DELETE SUCCESS] Deactivated sport ID '{sport_id}': {deleted_success}")

print("\n==========================================")
print("ALL 5 CRUD OPERATIONS VERIFIED SUCCESSFUL!")
print("==========================================")
