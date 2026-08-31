from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any

# ==========================================
# 1. USER PYDANTIC MODELS (User Management)
# ==========================================

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Jane Doe"})
    email: str = Field(..., json_schema_extra={"example": "jane.doe@example.com"})
    age: int = Field(..., ge=1, le=120, json_schema_extra={"example": 28})
    role: Optional[str] = Field(default="Parent", json_schema_extra={"example": "Parent"})

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format. Must contain '@' and a domain extension.")
        return v


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    age: Optional[int] = Field(None, ge=1, le=120)
    role: Optional[str] = None


class UserOut(UserBase):
    id: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================
# 2. SPORTS PYDANTIC MODELS (Summer Camp)
# ==========================================

class SportBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    category: str = Field(..., json_schema_extra={"example": "Team Sports"})
    description: str = Field(..., min_length=10)
    min_age: int = Field(..., ge=3, le=25)
    max_age: int = Field(..., ge=3, le=25)
    instructor: str = Field(..., min_length=2)
    schedule_days: str = Field(..., json_schema_extra={"example": "Mon, Wed, Fri"})
    schedule_time: str = Field(..., json_schema_extra={"example": "09:00 AM - 11:00 AM"})
    location: str = Field(..., min_length=3)
    fee: float = Field(..., ge=0.0)
    max_capacity: int = Field(..., ge=1, le=500)
    image_icon: Optional[str] = Field(default="⚽")
    is_active: Optional[bool] = Field(default=True)

    @field_validator('max_age')
    @classmethod
    def validate_age_range(cls, v: int, info) -> int:
        if 'min_age' in info.data and v < info.data['min_age']:
            raise ValueError(f"Max age ({v}) cannot be less than Min age ({info.data['min_age']}).")
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
    id: Any
    slug_id: Optional[str] = None
    enrolled_count: int = 0
    created_at: Optional[str] = None


# ==========================================
# 3. ENROLLMENT PYDANTIC MODELS
# ==========================================

class EnrollmentCreate(BaseModel):
    sport_id: Any = Field(..., json_schema_extra={"example": "junior-soccer-champions"})
    participant_name: str = Field(..., min_length=2, max_length=100)
    participant_age: int = Field(..., ge=3, le=25)
    parent_name: str = Field(..., min_length=2, max_length=100)
    parent_email: str = Field(...)
    parent_phone: str = Field(..., min_length=7, max_length=20)
    participant_grade: Optional[str] = Field(default="N/A")
    tshirt_size: Optional[str] = Field(default="M")
    medical_notes: Optional[str] = Field(default="None")
    emergency_contact: Optional[str] = Field(default="N/A")
    payment_method: Optional[str] = Field(default="Full Payment")


class EnrollmentOut(BaseModel):
    id: Any
    enrollment_code: str
    sport_id: Any
    participant_name: str
    participant_age: int
    participant_grade: Optional[str] = None
    tshirt_size: Optional[str] = None
    medical_notes: Optional[str] = None
    parent_name: str
    parent_email: str
    parent_phone: str
    emergency_contact: Optional[str] = None
    payment_method: Optional[str] = None
    amount_paid: float
    status: str
    enrolled_at: str
    sport: Optional[Dict[str, Any]] = None


# ==========================================
# 4. DASHBOARD STATS MODEL
# ==========================================

class StatsOut(BaseModel):
    total_sports: int
    active_sports: int
    total_enrollments: int
    confirmed_enrollments: int
    cancelled_enrollments: int
    total_revenue: float
    spots_available: int
    popular_sports: List[Dict[str, Any]]
