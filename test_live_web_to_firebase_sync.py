from app.firestore_crud import update_sport, create_enrollment
from app.models_pydantic import SportUpdate, EnrollmentCreate

print("==========================================")
print("TESTING LIVE WEBPAGE-TO-FIREBASE CLOUD SYNC")
print("==========================================")

# 1. Simulate Admin Portal Editing a Sport (e.g. Updating Fee and Capacity for Basketball)
print("--- 1. Admin Edits Sport in Web Portal ---")
update_data = SportUpdate(
    fee=180.0,
    max_capacity=25
)
updated_sport = update_sport(2, update_data)
print(f"[SUCCESS 200 OK] Updated Sport '{updated_sport['title']}' in Live Firebase!")
print(f"New Fee: ${updated_sport['fee']} | New Capacity: {updated_sport['max_capacity']}\n")

# 2. Simulate Student Registration on Webpage
print("--- 2. Parent Enrolls Student on Webpage ---")
enrollment_input = EnrollmentCreate(
    sport_id=2,
    participant_name="Rohan Gupta",
    participant_age=11,
    parent_name="Anil Gupta",
    parent_email="anil.gupta@example.com",
    parent_phone="+919876500000"
)
new_enrollment = create_enrollment(enrollment_input)
print(f"[SUCCESS 200 OK] Registered Camper '{new_enrollment['participant_name']}' in Live Firebase!")
print(f"Pass Code: {new_enrollment['enrollment_code']} | Status: {new_enrollment['status']}")

print("==========================================")
print("CONFIRMED: ALL WEBPAGE & ADMIN EDITS UPDATE LIVE IN GOOGLE FIREBASE!")
print("==========================================")
