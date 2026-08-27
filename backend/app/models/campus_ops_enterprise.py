"""
Campus Operations Models: Hostel Accommodation, Library Catalog, and Fleet Transport.
"""
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, Date, DateTime,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from app.models.base_enterprise import BaseModel, Base


class RoomType(str, enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    DORMITORY = "dormitory"


class HostelBuilding(BaseModel):
    """Hostel / Dormitory Hall of Residence."""
    __tablename__ = "hostel_buildings"

    name = Column(String(150), nullable=False)
    code = Column(String(50), nullable=False)
    gender_type = Column(String(50), default="co-ed") # male, female, co-ed
    warden_name = Column(String(150), nullable=True)
    warden_contact = Column(String(50), nullable=True)
    total_floors = Column(Integer, default=4)
    total_rooms = Column(Integer, default=100)
    amenities = Column(JSONB, default=list) # ["WiFi", "Laundry", "Gym", "Mess"]

    rooms = relationship("HostelRoom", back_populates="building", cascade="all, delete-orphan")


class HostelRoom(BaseModel):
    """Room inside a hostel building."""
    __tablename__ = "hostel_rooms"

    building_id = Column(String(36), ForeignKey("hostel_buildings.id", ondelete="CASCADE"), nullable=False)
    room_number = Column(String(50), nullable=False)
    floor_number = Column(Integer, default=1)
    room_type = Column(Enum(RoomType), default=RoomType.DOUBLE, nullable=False)
    capacity = Column(Integer, default=2, nullable=False)
    occupied_count = Column(Integer, default=0, nullable=False)
    monthly_rent = Column(Float, default=500.0)
    has_attached_bath = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    building = relationship("HostelBuilding", back_populates="rooms")
    allocations = relationship("BedAllocation", back_populates="room")


class BedAllocation(BaseModel):
    """Student bed allocation in a hostel room."""
    __tablename__ = "bed_allocations"

    room_id = Column(String(36), ForeignKey("hostel_rooms.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    bed_number = Column(String(20), nullable=False)
    start_date = Column(Date, default=date.today, nullable=False)
    end_date = Column(Date, nullable=True)
    is_vacated = Column(Boolean, default=False)

    room = relationship("HostelRoom", back_populates="allocations")


class LibraryBook(BaseModel):
    """Library book catalog item."""
    __tablename__ = "library_books"

    isbn = Column(String(50), nullable=False)
    title = Column(String(300), nullable=False)
    author = Column(String(255), nullable=False)
    publisher = Column(String(200), nullable=True)
    edition = Column(String(50), nullable=True)
    publication_year = Column(Integer, nullable=True)
    genre = Column(String(100), nullable=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    shelf_location = Column(String(100), nullable=True)

    issues = relationship("BookIssue", back_populates="book")


class BookIssue(BaseModel):
    """Borrowing record for a library book."""
    __tablename__ = "book_issues"

    book_id = Column(String(36), ForeignKey("library_books.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    fine_amount = Column(Float, default=0.0)
    status = Column(String(50), default="issued") # issued, returned, lost, overdue

    book = relationship("LibraryBook", back_populates="issues")


class TransportRoute(BaseModel):
    """Campus shuttle / bus transit route."""
    __tablename__ = "transport_routes"

    route_name = Column(String(150), nullable=False)
    route_code = Column(String(50), nullable=False)
    vehicle_number = Column(String(50), nullable=False)
    driver_name = Column(String(150), nullable=True)
    driver_contact = Column(String(50), nullable=True)
    total_capacity = Column(Integer, default=40)
    stops = Column(JSONB, default=list) # [{"stop_name": "Downtown", "time": "07:30 AM", "lat": 0, "lng": 0}]
