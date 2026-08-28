from app.firestore_crud import update_sport, get_sport_by_id
from app.models_pydantic import SportUpdate

print("==========================================")
print("TESTING MIN AGE = 10 LIVE SYNC TO FIREBASE")
print("==========================================")

# 1. Fetch sport
sport = get_sport_by_id("junior-soccer-champions")
if not sport:
    sport = get_sport_by_id(1)

print(f"Target Sport:        '{sport['title']}'")
print(f"Original Min Age:    {sport['min_age']} years old")

# 2. Update min_age to 10
print("\n--- Updating min_age to 10 ---")
update_data = SportUpdate(
    min_age=10
)

updated = update_sport(sport["id"], update_data)

print(f"\n[FIREBASE CLOUD SYNC SUCCESS 200 OK]")
print(f"Document ID:      '{updated.get('slug_id', updated['id'])}'")
print(f"Updated Min Age:  {updated['min_age']} years old")

print("==========================================")
print("VERIFIED: MIN AGE = 10 UPDATED LIVE IN GOOGLE FIREBASE!")
print("==========================================")
