from app.database import SessionLocal, Base, engine
from app.models import Sport, Enrollment
from app.crud import create_enrollment
from app.schemas import EnrollmentCreate

SAMPLE_SPORTS = [
    {
        "title": "Junior Soccer Champions",
        "category": "Team Sports",
        "description": "Comprehensive soccer training focusing on footwork, dribbling, tactical plays, and fun team matches.",
        "min_age": 6,
        "max_age": 12,
        "instructor": "Coach Alex Morgan",
        "schedule_days": "Mon, Wed, Fri",
        "schedule_time": "09:00 AM - 11:00 AM",
        "location": "Main Turf Pitch A",
        "fee": 160.0,
        "max_capacity": 20,
        "image_icon": "⚽"
    },
    {
        "title": "Summer Hoops Basketball Academy",
        "category": "Team Sports",
        "description": "Master shooting drills, defense, fast breaks, and teamwork on indoor maple courts with pro coaches.",
        "min_age": 8,
        "max_age": 16,
        "instructor": "Coach Marcus Vance",
        "schedule_days": "Tue, Thu, Sat",
        "schedule_time": "10:00 AM - 12:00 PM",
        "location": "Indoor Arena Court 1",
        "fee": 175.0,
        "max_capacity": 18,
        "image_icon": "🏀"
    },
    {
        "title": "AquaSplash Swimming & Water Safety",
        "category": "Water Sports",
        "description": "Learn stroke refinement, breathing techniques, diving basics, and water survival skills safely.",
        "min_age": 5,
        "max_age": 14,
        "instructor": "Coach Elena Rostova",
        "schedule_days": "Mon, Tue, Wed, Thu",
        "schedule_time": "08:30 AM - 10:00 AM",
        "location": "Olympic Heated Pool",
        "fee": 200.0,
        "max_capacity": 15,
        "image_icon": "🏊‍♂️"
    },
    {
        "title": "Elite Tennis Stars Camp",
        "category": "Racket Sports",
        "description": "Develop forehands, backhands, serves, and court movement with mini-tournaments each week.",
        "min_age": 7,
        "max_age": 15,
        "instructor": "Coach David Miller",
        "schedule_days": "Mon, Wed, Fri",
        "schedule_time": "04:00 PM - 06:00 PM",
        "location": "Hard Courts 3 & 4",
        "fee": 185.0,
        "max_capacity": 12,
        "image_icon": "🎾"
    },
    {
        "title": "Martial Arts & Taekwondo Fundamentals",
        "category": "Combat & Fitness",
        "description": "Build discipline, self-defense, agility, and respect through form practice and light sparring.",
        "min_age": 6,
        "max_age": 13,
        "instructor": "Master Chen Wei",
        "schedule_days": "Tue, Thu",
        "schedule_time": "02:00 PM - 03:30 PM",
        "location": "Dojo Pavilion",
        "fee": 140.0,
        "max_capacity": 16,
        "image_icon": "🥋"
    },
    {
        "title": "Outdoor Archery & Target Shooting",
        "category": "Outdoor & Track",
        "description": "Focus, precision, and safety training using recurve bows under expert range instruction.",
        "min_age": 10,
        "max_age": 17,
        "instructor": "Instructor Robin Hayes",
        "schedule_days": "Mon, Thu",
        "schedule_time": "01:00 PM - 03:00 PM",
        "location": "Archery Range West",
        "fee": 190.0,
        "max_capacity": 10,
        "image_icon": "🏹"
    },
    {
        "title": "Gymnastics & Tumbling Stars",
        "category": "Combat & Fitness",
        "description": "Improve flexibility, balance, cartwheels, beam routines, and vault landings in a padded studio.",
        "min_age": 5,
        "max_age": 12,
        "instructor": "Coach Maya Lin",
        "schedule_days": "Wed, Fri",
        "schedule_time": "11:00 AM - 12:30 PM",
        "location": "Gymnastics Hall B",
        "fee": 165.0,
        "max_capacity": 14,
        "image_icon": "🤸‍♀️"
    },
    {
        "title": "Beach Volleyball League",
        "category": "Team Sports",
        "description": "Bump, set, spike! Learn beach volleyball strategies, serve control, and active outdoor fitness.",
        "min_age": 11,
        "max_age": 17,
        "instructor": "Coach Spike Johnson",
        "schedule_days": "Tue, Fri",
        "schedule_time": "03:30 PM - 05:30 PM",
        "location": "Sand Courts 1 & 2",
        "fee": 150.0,
        "max_capacity": 16,
        "image_icon": "🏐"
    }
]

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if sports already exist
        if db.query(Sport).count() == 0:
            print("Seeding initial sports activities...")
            created_sports = []
            for item in SAMPLE_SPORTS:
                sport = Sport(**item)
                db.add(sport)
                created_sports.append(sport)
            db.commit()

            print(f"Successfully seeded {len(SAMPLE_SPORTS)} sports!")

            # Seed a couple sample enrollments for realistic stats
            soccer = db.query(Sport).filter(Sport.title.like("%Soccer%")).first()
            swimming = db.query(Sport).filter(Sport.title.like("%Swimming%")).first()

            if soccer:
                create_enrollment(db, EnrollmentCreate(
                    sport_id=soccer.id,
                    participant_name="Leo Fernandez",
                    participant_age=9,
                    participant_grade="4th Grade",
                    tshirt_size="M",
                    medical_notes="None",
                    parent_name="Carlos Fernandez",
                    parent_email="carlos.f@example.com",
                    parent_phone="+1-555-0144",
                    emergency_contact="+1-555-9911 (Mother)",
                    payment_method="Full Payment"
                ))
            if swimming:
                create_enrollment(db, EnrollmentCreate(
                    sport_id=swimming.id,
                    participant_name="Emily Watson",
                    participant_age=8,
                    participant_grade="3rd Grade",
                    tshirt_size="S",
                    medical_notes="Wears earplugs in pool",
                    parent_name="Jane Watson",
                    parent_email="jane.watson@example.com",
                    parent_phone="+1-555-0188",
                    emergency_contact="+1-555-8822 (Father)",
                    payment_method="Full Payment"
                ))
            print("Successfully seeded sample enrollments!")
        else:
            print("Database already contains data, skipping seed.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
