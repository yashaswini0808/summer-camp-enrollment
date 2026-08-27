import random
import string
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from fastapi import HTTPException, status
from app.models import Sport, Enrollment
from app.schemas import SportCreate, SportUpdate, EnrollmentCreate

def generate_enrollment_code() -> str:
    """Generates a random unique enrollment code, e.g. CAMP-2026-X89A"""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=5))
    return f"CAMP-2026-{suffix}"

# --- Sports CRUD ---

def get_sports(
    db: Session,
    category: Optional[str] = None,
    age: Optional[int] = None,
    search: Optional[str] = None,
    active_only: bool = True
) -> List[Sport]:
    query = db.query(Sport)
    
    if active_only:
        query = query.filter(Sport.is_active == True)
        
    if category and category != "All":
        query = query.filter(Sport.category == category)
        
    if age is not None:
        query = query.filter(and_(Sport.min_age <= age, Sport.max_age >= age))
        
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Sport.title.ilike(search_pattern),
                Sport.description.ilike(search_pattern),
                Sport.instructor.ilike(search_pattern),
                Sport.location.ilike(search_pattern)
            )
        )
        
    return query.order_by(Sport.id.asc()).all()

def get_sport_by_id(db: Session, sport_id: int) -> Optional[Sport]:
    return db.query(Sport).filter(Sport.id == sport_id).first()

def create_sport(db: Session, sport_data: SportCreate) -> Sport:
    db_sport = Sport(**sport_data.model_dump())
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport

def update_sport(db: Session, sport_id: int, sport_data: SportUpdate) -> Sport:
    db_sport = get_sport_by_id(db, sport_id)
    if not db_sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID {sport_id} not found."
        )
    
    update_dict = sport_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_sport, key, value)
        
    db.commit()
    db.refresh(db_sport)
    return db_sport

def delete_sport(db: Session, sport_id: int) -> bool:
    db_sport = get_sport_by_id(db, sport_id)
    if not db_sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID {sport_id} not found."
        )
    # Soft delete
    db_sport.is_active = False
    db.commit()
    return True


# --- Enrollment CRUD & Validations ---

def create_enrollment(db: Session, data: EnrollmentCreate) -> Enrollment:
    # 1. Fetch sport and validate existence & active status
    sport = db.query(Sport).filter(Sport.id == data.sport_id).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sport with ID {data.sport_id} does not exist."
        )
        
    if not sport.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The sport '{sport.title}' is currently inactive or unavailable for enrollment."
        )

    # 2. Validate Participant Age eligibility
    if data.participant_age < sport.min_age or data.participant_age > sport.max_age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Age Validation Failed: Participant age ({data.participant_age}) is outside the permitted age range for {sport.title} ({sport.min_age} - {sport.max_age} years old)."
        )

    # 3. Validate Sport Capacity
    if sport.enrolled_count >= sport.max_capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Capacity Limit Reached: '{sport.title}' has reached its maximum capacity of {sport.max_capacity} participants."
        )

    # 4. Validate Duplicate Enrollment (Same participant name + parent email + sport_id + status CONFIRMED)
    existing = db.query(Enrollment).filter(
        and_(
            Enrollment.sport_id == data.sport_id,
            func.lower(Enrollment.participant_name) == data.participant_name.strip().lower(),
            func.lower(Enrollment.parent_email) == data.parent_email.strip().lower(),
            Enrollment.status == "CONFIRMED"
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Duplicate Enrollment: '{data.participant_name}' is already enrolled in '{sport.title}' under code {existing.enrollment_code}."
        )

    # 5. Generate Unique Code
    code = generate_enrollment_code()
    while db.query(Enrollment).filter(Enrollment.enrollment_code == code).first():
        code = generate_enrollment_code()

    # 6. Create enrollment record and increment sport capacity
    db_enrollment = Enrollment(
        enrollment_code=code,
        sport_id=data.sport_id,
        participant_name=data.participant_name.strip(),
        participant_age=data.participant_age,
        participant_grade=data.participant_grade,
        tshirt_size=data.tshirt_size,
        medical_notes=data.medical_notes,
        parent_name=data.parent_name.strip(),
        parent_email=data.parent_email.strip().lower(),
        parent_phone=data.parent_phone.strip(),
        emergency_contact=data.emergency_contact.strip(),
        payment_method=data.payment_method,
        amount_paid=sport.fee,
        status="CONFIRMED"
    )

    sport.enrolled_count += 1
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_enrollments(
    db: Session,
    parent_email: Optional[str] = None,
    parent_phone: Optional[str] = None,
    participant_name: Optional[str] = None,
    sport_id: Optional[int] = None,
    status_filter: Optional[str] = None
) -> List[Enrollment]:
    query = db.query(Enrollment)

    if parent_email:
        query = query.filter(func.lower(Enrollment.parent_email) == parent_email.strip().lower())
    if parent_phone:
        query = query.filter(Enrollment.parent_phone.contains(parent_phone.strip()))
    if participant_name:
        query = query.filter(Enrollment.participant_name.ilike(f"%{participant_name.strip()}%"))
    if sport_id:
        query = query.filter(Enrollment.sport_id == sport_id)
    if status_filter and status_filter != "ALL":
        query = query.filter(Enrollment.status == status_filter.upper())

    return query.order_by(Enrollment.enrolled_at.desc()).all()

def get_enrollment_by_code(db: Session, code: str) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(func.upper(Enrollment.enrollment_code) == code.strip().upper()).first()

def cancel_enrollment(db: Session, enrollment_id: int) -> Enrollment:
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment record with ID {enrollment_id} not found."
        )

    if enrollment.status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This enrollment has already been cancelled."
        )

    enrollment.status = "CANCELLED"
    sport = db.query(Sport).filter(Sport.id == enrollment.sport_id).first()
    if sport and sport.enrolled_count > 0:
        sport.enrolled_count -= 1

    db.commit()
    db.refresh(enrollment)
    return enrollment


# --- Analytics & Dashboard Stats ---

def get_dashboard_stats(db: Session):
    total_sports = db.query(Sport).count()
    active_sports = db.query(Sport).filter(Sport.is_active == True).count()
    total_enrollments = db.query(Enrollment).count()
    confirmed_enrollments = db.query(Enrollment).filter(Enrollment.status == "CONFIRMED").count()
    cancelled_enrollments = db.query(Enrollment).filter(Enrollment.status == "CANCELLED").count()

    # Revenue from confirmed enrollments
    revenue_query = db.query(func.sum(Enrollment.amount_paid)).filter(Enrollment.status == "CONFIRMED").scalar()
    total_revenue = float(revenue_query) if revenue_query else 0.0

    # Total spots vs enrolled
    sports = db.query(Sport).filter(Sport.is_active == True).all()
    total_capacity = sum(s.max_capacity for s in sports)
    total_enrolled = sum(s.enrolled_count for s in sports)
    spots_available = max(0, total_capacity - total_enrolled)

    # Popular sports
    popular_sports = []
    for s in sports:
        popular_sports.append({
            "id": s.id,
            "title": s.title,
            "category": s.category,
            "enrolled_count": s.enrolled_count,
            "max_capacity": s.max_capacity,
            "fee": s.fee
        })
    popular_sports.sort(key=lambda x: x["enrolled_count"], reverse=True)

    return {
        "total_sports": total_sports,
        "active_sports": active_sports,
        "total_enrollments": total_enrollments,
        "confirmed_enrollments": confirmed_enrollments,
        "cancelled_enrollments": cancelled_enrollments,
        "total_revenue": total_revenue,
        "spots_available": spots_available,
        "popular_sports": popular_sports[:6]
    }
