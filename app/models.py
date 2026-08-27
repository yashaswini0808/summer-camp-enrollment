from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=False)
    min_age = Column(Integer, nullable=False, default=5)
    max_age = Column(Integer, nullable=False, default=18)
    instructor = Column(String(100), nullable=False)
    schedule_days = Column(String(100), nullable=False)
    schedule_time = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    fee = Column(Float, nullable=False, default=0.0)
    max_capacity = Column(Integer, nullable=False, default=20)
    enrolled_count = Column(Integer, nullable=False, default=0)
    image_icon = Column(String(50), nullable=False, default="⚽")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship("Enrollment", back_populates="sport", cascade="all, delete-orphan")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_code = Column(String(30), unique=True, nullable=False, index=True)
    sport_id = Column(Integer, ForeignKey("sports.id", ondelete="CASCADE"), nullable=False)
    
    participant_name = Column(String(100), nullable=False, index=True)
    participant_age = Column(Integer, nullable=False)
    participant_grade = Column(String(50), nullable=True)
    tshirt_size = Column(String(20), nullable=False, default="M")
    medical_notes = Column(Text, nullable=True)

    parent_name = Column(String(100), nullable=False)
    parent_email = Column(String(120), nullable=False, index=True)
    parent_phone = Column(String(30), nullable=False, index=True)
    emergency_contact = Column(String(100), nullable=False)

    payment_method = Column(String(50), nullable=False, default="Full Payment")
    amount_paid = Column(Float, nullable=False, default=0.0)
    status = Column(String(30), nullable=False, default="CONFIRMED") # CONFIRMED, CANCELLED
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    sport = relationship("Sport", back_populates="enrollments")
