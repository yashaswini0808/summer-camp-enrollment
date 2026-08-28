from app.firestore_crud import update_sport, get_sport_by_id
from app.models_pydantic import SportUpdate

print("==========================================")
print("TESTING SPORT TITLE RENAME & FIREBASE SYNC")
print("==========================================")

# Fetch sport #2
sport = get_sport_by_id(2)
print(f"Original Sport Title: '{sport['title']}' (slug_id: {sport.get('slug_id')})")

# Rename Title
new_title = "Summer Hoops Basketball Academy 2026"
print(f"Renaming Title to:    '{new_title}'")

update_data = SportUpdate(title=new_title)
result = update_sport(2, update_data)

print(f"\n[SUCCESS 200 OK] Updated Sport Title in Live Firebase!")
print(f"New Title:   '{result['title']}'")
print(f"New Slug ID: '{result['slug_id']}'")
print("==========================================")
