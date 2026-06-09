from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

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
        DateTime,
        default=datetime.utcnow
    )

    must_change_password = Column(
        Boolean,
        default=False
    )

    predictions = relationship(
        "Prediction",
        back_populates="user"
    )

    tournament_prediction = relationship(
        "TournamentPrediction",
        back_populates="user",
        uselist=False
    )

class Match(Base):

    __tablename__ = "matches"

    match_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    home_team = Column(
        String(100),
        nullable=False
    )

    away_team = Column(
        String(100),
        nullable=False
    )

    stage = Column(
        String(50),
        nullable=False
    )

    kickoff_time = Column(
        DateTime,
        nullable=False
    )

    home_score = Column(
        Integer,
        nullable=True
    )

    away_score = Column(
        Integer,
        nullable=True
    )

    result_entered = Column(
        Boolean,
        default=False
    )
    
    is_visible = Column(
    Boolean,
    default=False,
    nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    qualified_team = Column(
        String(100),
        nullable=True
    )

    predictions = relationship(
        "Prediction",
        back_populates="match"
    )
   

class Prediction(Base):

    __tablename__ = "predictions"

    prediction_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    match_id = Column(
        Integer,
        ForeignKey("matches.match_id", ondelete="CASCADE"),
        nullable=False
    )

    pred_home = Column(
        Integer,
        nullable=False
    )

    pred_away = Column(
        Integer,
        nullable=False
    )

    submitted_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    pred_qualified_team = Column(
        String(100),
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="predictions"
    )

    match = relationship(
        "Match",
        back_populates="predictions"
    )

    __table_args__ = (
        # Ensure a user can only submit one prediction per match
        UniqueConstraint(
            'user_id',
            'match_id',
            name="unique_user_match_prediction"),
    )

class TournamentPrediction(Base):
    
    __tablename__ = "tournament_predictions"

    prediction_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    champion = Column(
        String(100),        
    )

    runner_up = Column(
        String(100),
    )

    submitted_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="tournament_prediction"
    )

class ScoringRule(Base):

    __tablename__ = "scoring_rules"

    rule_key = Column(
        String(100),
        primary_key=True,
    )

    rule_value = Column(
        Integer,
        nullable=False
    )

class Admin(Base):

    __tablename__ = "admins"

    admin_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True
    )

    password_hash = Column(
        String(255)
    )