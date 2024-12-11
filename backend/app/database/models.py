from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import text
from sqlmodel import Field, SQLModel, Relationship


# Define enums for roles and other enumerations
class UserRole(str, Enum):
    STUDENT = "Student"
    ADMIN = "Admin"
    SUPER_ADMIN = "SuperAdmin"
    TUTOR = "Tutor"


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class ProductCategory(str, Enum):
    VEGETABLES = "Vegetables"
    FRUITS = "Fruits"
    SEEDS = "Seeds"
    DAIRY = "Dairy"
    MEAT = "Meat"
    EQUIPMENT = "Equipment"


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"


class AbstractTimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)")
        }
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)")
        }
    )


# User model
class User(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str
    email: str = Field(index=True, unique=True)
    phone: str = Field(unique=True)
    password_hashed: str
    role: UserRole
    is_active: bool = Field(default=True)

    # Relationships
    verification_codes: List["VerificationCode"] = Relationship(back_populates="user")
    messages_sent: List["Message"] = Relationship(back_populates="sender")


# Chat model
class Chat(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    buyer_id: int = Field(foreign_key="user.id")
    farmer_id: int = Field(foreign_key="user.id")

    messages: List["Message"] = Relationship(back_populates="chat")


# Message model
class Message(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")
    sender_id: int = Field(foreign_key="user.id")
    content: str

    chat: Chat = Relationship(back_populates="messages")
    sender: User = Relationship(back_populates="messages_sent")


# VerificationCode model
class VerificationCode(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    email: str = Field(index=True)
    code: str
    purpose: str  # e.g., 'registration' or 'login'
    expires_at: datetime

    user: User = Relationship(back_populates="verification_codes")


# Project model
class Project(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    owner_id: int = Field(foreign_key="user.id")


# ProjectDatabase model
class ProjectDatabase(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    owner_id: int = Field(foreign_key="user.id")
    project_id: int = Field(foreign_key="project.id")
    connection_url: Optional[str] = None
    connection_user: Optional[str] = None
    connection_password: Optional[str] = None
    chat_id: Optional[int] = Field(default=None, foreign_key="chat.id")


# ProjectTable placeholder
class ProjectTable(AbstractTimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Define additional fields here as required
