from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator

# --- Sport Schemas ---

class SportBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Junior Soccer Academy"})
    category: str = Field(..., json_schema_extra={"example": "Team Sports"})
    description: str = Field(..., json_schema_extra={"example": "Dynamic soccer training focusing on fundamentals, footwork, and teamwork."})
    min_age: int = Field(..., ge=3, le=25, json_schema_extra={"example": 6})
    max_age: int = Field(..., ge=3, le=25, json_schema_extra={"example": 14})
    instructor: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Coach Alex Morgan"})
    schedule_days: str = Field(..., json_schema_extra={"example": "Mon, Wed, Fri"})
    schedule_time: str = Field(..., json_schema_extra={"example": "09:00 AM - 11:00 AM"})
    location: str = Field(..., json_schema_extra={"example": "Main Turf Pitch A"})
    fee: float = Field(..., ge=0.0, json_schema_extra={"example": 150.0})
    max_capacity: int = Field(..., ge=1, le=500, json_schema_extra={"example": 25})
    image_icon: str = Field(default="⚽", json_schema_extra={"example": "⚽"})
    is_active: bool = Field(default=True)

    @field_validator('max_age')
    @classmethod
    def validate_age_range(cls, v, info):
        min_age = info.data.get('min_age')
        if min_age is not None and v < min_age:
            raise ValueError('max_age must be greater than or equal to min_age')
        return v

class SportCreate(SportBase):
    pass

class SportUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    instructor: Optional[str] = None
    schedule_days: Optional[str] = None
    schedule_time: Optional[str] = None
    location: Optional[str] = None
    fee: Optional[float] = None
    max_capacity: Optional[int] = None
    image_icon: Optional[str] = None
    is_active: Optional[bool] = None

class SportOut(SportBase):
    id: Union[int, str]
    enrolled_count: int = 0
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Enrollment Schemas ---

class EnrollmentCreate(BaseModel):
    sport_id: Union[int, str] = Field(..., json_schema_extra={"example": 1})
    participant_name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Sammy Taylor"})
    participant_age: int = Field(..., ge=3, le=25, json_schema_extra={"example": 10})
    participant_grade: Optional[str] = Field(None, json_schema_extra={"example": "5th Grade"})
    tshirt_size: str = Field(default="M", json_schema_extra={"example": "M"})
    medical_notes: Optional[str] = Field(None, json_schema_extra={"example": "Asthma inhaler as needed"})

    parent_name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Sarah Taylor"})
    parent_email: str = Field(..., json_schema_extra={"example": "sarah.taylor@example.com"})
    parent_phone: str = Field(..., min_length=7, max_length=20, json_schema_extra={"example": "+1-555-0192"})
    emergency_contact: str = Field(..., min_length=7, max_length=100, json_schema_extra={"example": "+1-555-9988 (Grandmother)"})
    payment_method: str = Field(default="Full Payment", json_schema_extra={"example": "Full Payment"})

    @field_validator('parent_email')
    @classmethod
    def validate_email_format(cls, v):
        v = v.strip().lower()
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v

class EnrollmentOut(BaseModel):
    id: Union[int, str]
    enrollment_code: str
    sport_id: Union[int, str]
    participant_name: str
    participant_age: int
    participant_grade: Optional[str] = None
    tshirt_size: str
    medical_notes: Optional[str] = None
    parent_name: str
    parent_email: str
    parent_phone: str
    emergency_contact: str
    payment_method: str
    amount_paid: float
    status: str
    enrolled_at: str
    sport: Optional[SportOut] = None

    model_config = ConfigDict(from_attributes=True)


# --- Analytics Schemas ---

class TopSportStat(BaseModel):
    id: Union[int, str]
    title: str
    category: str
    enrolled_count: int
    max_capacity: int
    fee: float

class StatsOut(BaseModel):
    total_sports: int
    active_sports: int
    total_enrollments: int
    confirmed_enrollments: int
    cancelled_enrollments: int
    total_revenue: float
    spots_available: int
    popular_sports: List[TopSportStat]
