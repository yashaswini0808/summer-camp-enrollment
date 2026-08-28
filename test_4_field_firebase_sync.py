from app.firestore_crud import create_enrollment
from app.models_pydantic import EnrollmentCreate

print("==========================================")
print("TESTING 4-FIELD ENROLLMENT LIVE FIREBASE SYNC")
print("==========================================")

# Create enrollment with the exact 4 fields requested
enrollment_data = EnrollmentCreate(
    sport_id=3,  # AquaSplash Swimming
    participant_name="Aarav Sharma",
    participant_age=9,
    parent_name="Priya Sharma",
    parent_email="priya.sharma@example.com",
    parent_phone="+919876543210"
)

result = create_enrollment(enrollment_data)

print(f"[SUCCESS 200 OK] Created & Uploaded to Live Firebase!")
print(f"Camper Name:     {result['participant_name']} ({result['participant_age']} yrs)")
print(f"Parent Name:     {result['parent_name']} ({result['parent_email']})")
print(f"Enrollment Code: {result['enrollment_code']}")
print(f"Sport Title:     {result['sport']['title']}")
print("==========================================")
