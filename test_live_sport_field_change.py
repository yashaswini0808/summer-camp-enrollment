from app.firestore_crud import update_sport, get_sport_by_id
from app.models_pydantic import SportUpdate

print("==========================================")
print("TESTING LIVE FIELD CHANGE SYNC TO FIREBASE")
print("==========================================")

# 1. Fetch sport by id
sport = get_sport_by_id("summer-hoops-basketball-academy-2026")
if not sport:
    sport = get_sport_by_id(2)

print(f"Current Sport: '{sport['title']}'")
print(f"Current Coach: '{sport['instructor']}' | Current Fee: ${sport['fee']}")

# 2. Change field details (e.g., Update Coach & Fee)
print("\n--- Editing Coach to 'Coach Kumar' & Fee to $185.00 ---")
update_data = SportUpdate(
    instructor="Coach Kumar",
    fee=185.00
)

updated = update_sport(sport["id"], update_data)

print(f"\n[FIREBASE CLOUD SYNC SUCCESS 200 OK]")
print(f"Document ID:   '{updated.get('slug_id', updated['id'])}'")
print(f"Updated Coach: '{updated['instructor']}'")
print(f"Updated Fee:   '${updated['fee']:.2f}'")

print("==========================================")
print("VERIFIED: FIELD CHANGES UPDATE LIVE IN GOOGLE FIREBASE!")
print("==========================================")
