"""
Trimly API — SQLAlchemy models for Users and Salons
"""
import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    Boolean, Column, DateTime, Decimal, ForeignKey,
    Integer, String, Text, ARRAY, JSON, Time, func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from core.database import Base


def uuid_pk():
    """Default UUID primary key."""
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def now_utc():
    """Server-side UTC timestamp default."""
    return Column(DateTime(timezone=True), server_default=func.now())


class TimestampMixin:
    """Reusable created_at + updated_at columns."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = uuid_pk()
    phone = Column(String(15), unique=True, nullable=False, index=True)
    name = Column(String(100))
    email = Column(String(255))
    role = Column(String(20), nullable=False, default="CUSTOMER")
    avatar_url = Column(Text)
    language = Column(String(10), default="ur")
    timezone = Column(String(50), default="Asia/Karachi")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    owned_salons = relationship("Salon", back_populates="owner", foreign_keys="Salon.owner_id")
    barber_profile = relationship("Barber", back_populates="user", uselist=False)
    customer_profiles = relationship("Customer", back_populates="user")


class Salon(Base, TimestampMixin):
    __tablename__ = "salons"

    id = uuid_pk()
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    type = Column(String(30), nullable=False)
    phone = Column(String(15))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(50))
    area = Column(String(100))
    latitude = Column(Decimal(10, 8))
    longitude = Column(Decimal(11, 8))
    logo_url = Column(Text)
    cover_url = Column(Text)
    description = Column(Text)

    # Business settings
    currency = Column(String(5), default="PKR")
    timezone = Column(String(50), default="Asia/Karachi")
    opening_time = Column(Time, default="09:00:00")
    closing_time = Column(Time, default="21:00:00")
    working_days = Column(ARRAY(Integer), default=[1, 2, 3, 4, 5, 6])

    # Loyalty config
    points_per_visit = Column(Integer, default=10)
    points_per_rupee = Column(Decimal(5, 2), default=0)
    loyalty_tiers_config = Column(JSONB, default={})

    # Reminder config
    reminder_days_haircut = Column(Integer, default=21)
    reminder_days_beard = Column(Integer, default=7)
    reminder_days_facial = Column(Integer, default=30)
    reminder_days_color = Column(Integer, default=45)

    # Feature flags
    queue_enabled = Column(Boolean, default=True)
    online_booking_enabled = Column(Boolean, default=True)
    loyalty_enabled = Column(Boolean, default=True)
    ai_reminders_enabled = Column(Boolean, default=False)
    whatsapp_enabled = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
    plan = Column(String(20), default="STARTER")
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    owner = relationship("User", back_populates="owned_salons", foreign_keys=[owner_id])
    branches = relationship("Branch", back_populates="salon")
    barbers = relationship("Barber", back_populates="salon")
    customers = relationship("Customer", back_populates="salon")
    services = relationship("Service", back_populates="salon")
    chairs = relationship("Chair", back_populates="salon")


class Branch(Base, TimestampMixin):
    __tablename__ = "branches"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    address = Column(Text)
    city = Column(String(50))
    phone = Column(String(15))
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    opening_time = Column(Time)
    closing_time = Column(Time)
    working_days = Column(ARRAY(Integer))
    is_active = Column(Boolean, default=True)
    is_main_branch = Column(Boolean, default=False)

    # Relationships
    salon = relationship("Salon", back_populates="branches")


class Barber(Base, TimestampMixin):
    __tablename__ = "barbers"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    name = Column(String(100), nullable=False)
    phone = Column(String(15))
    avatar_url = Column(Text)
    bio = Column(Text)
    experience_years = Column(Integer, default=0)
    specialties = Column(ARRAY(String))
    service_ids = Column(ARRAY(UUID(as_uuid=True)))

    status = Column(String(20), default="AVAILABLE")

    # Denormalized stats
    total_cuts = Column(Integer, default=0)
    total_revenue = Column(Decimal(12, 2), default=0)
    average_rating = Column(Decimal(3, 2), default=0)
    total_reviews = Column(Integer, default=0)

    commission_type = Column(String(20), default="FIXED")
    commission_value = Column(Decimal(8, 2), default=0)

    is_active = Column(Boolean, default=True)

    # Relationships
    salon = relationship("Salon", back_populates="barbers")
    user = relationship("User", back_populates="barber_profile")
    reviews = relationship("Review", back_populates="barber")


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(255))
    birthday = Column(DateTime(timezone=False))
    gender = Column(String(10))
    avatar_url = Column(Text)

    favorite_barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id"))
    favorite_service_id = Column(UUID(as_uuid=True))
    hair_preferences = Column(Text)
    notes = Column(Text)

    # Denormalized stats
    total_visits = Column(Integer, default=0)
    total_spent = Column(Decimal(12, 2), default=0)
    loyalty_points = Column(Integer, default=0)
    referral_code = Column(String(20), unique=True)
    referred_by_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))

    first_visit_at = Column(DateTime(timezone=True))
    last_visit_at = Column(DateTime(timezone=True))
    next_predicted_visit = Column(DateTime(timezone=True))
    churn_risk_score = Column(Decimal(3, 2), default=0)

    sms_consent = Column(Boolean, default=True)
    whatsapp_consent = Column(Boolean, default=True)
    call_consent = Column(Boolean, default=True)
    push_consent = Column(Boolean, default=True)

    tags = Column(ARRAY(String), default=[])
    is_active = Column(Boolean, default=True)

    # Relationships
    salon = relationship("Salon", back_populates="customers")
    user = relationship("User", back_populates="customer_profiles")
    appointments = relationship("Appointment", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")


class Service(Base, TimestampMixin):
    __tablename__ = "services"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)

    name = Column(String(100), nullable=False)
    name_ur = Column(String(200))
    description = Column(Text)
    category = Column(String(30))

    price = Column(Decimal(10, 2), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)

    image_url = Column(Text)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    reminder_days = Column(Integer)

    # Relationships
    salon = relationship("Salon", back_populates="services")


class Chair(Base, TimestampMixin):
    __tablename__ = "chairs"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id"))

    name = Column(String(50), nullable=False)
    number = Column(Integer)

    assigned_barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id"))
    current_status = Column(String(20), default="FREE")
    current_customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    service_started_at = Column(DateTime(timezone=True))
    service_estimated_end = Column(DateTime(timezone=True))

    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Relationships
    salon = relationship("Salon", back_populates="chairs")


class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id"))
    chair_id = Column(UUID(as_uuid=True), ForeignKey("chairs.id"))

    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    status = Column(String(20), default="PENDING")
    source = Column(String(20), default="OWNER")

    customer_notes = Column(Text)
    barber_notes = Column(Text)

    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    cancellation_reason = Column(Text)

    invoice_id = Column(UUID(as_uuid=True))

    # Relationships
    customer = relationship("Customer", back_populates="appointments")


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"

    id = uuid_pk()
    salon_id = Column(UUID(as_uuid=True), ForeignKey("salons.id"), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id"))
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"))

    overall_rating = Column(Integer, nullable=False)
    barber_rating = Column(Integer)
    comment = Column(Text)
    tags = Column(ARRAY(String), default=[])

    is_visible = Column(Boolean, default=True)
    owner_reply = Column(Text)
    replied_at = Column(DateTime(timezone=True))
    source = Column(String(20), default="APP")

    # Relationships
    customer = relationship("Customer", back_populates="reviews")
    barber = relationship("Barber", back_populates="reviews")
