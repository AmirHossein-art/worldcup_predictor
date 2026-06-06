from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String
)

from database.connection import Base

class User(Base):

    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    national_id = Column(
        String(10),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(11),
        unique=True,
        nullable=False
    )

    organization = Column(
        String(200),
        nullable=False
    )

    department = Column(
        String(200),
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime
    )