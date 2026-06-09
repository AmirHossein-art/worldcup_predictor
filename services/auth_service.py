from git import db
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from database.models import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password:str)-> str:
    return pwd_context.hash(password)

def verify_password(
        plain_password:str,
        hashed_password:str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def register_user(
    db: Session,
    first_name: str,
    last_name: str,
    national_id: str,
    phone: str,
    organization: str,
    department: str,
    password: str
):
    existing_user = (
    db.query(User)
    .filter(
        User.national_id == national_id
    )
    .first()
    )

    if existing_user:

        raise ValueError(
            "National ID already exists"
        )
    
    existing_phone = (
    db.query(User)
    .filter(
        User.phone == phone
    )
    .first()
    )

    if existing_phone:

        raise ValueError(
            "Phone already exists"
        )
    
    user = User(
    first_name=first_name,
    last_name=last_name,
    national_id=national_id,
    phone=phone,
    organization=organization,
    department=department,
    password_hash=hash_password(
        password
    ),
    is_verified=False,
    is_active=True,
    must_change_password=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(
    db: Session,
    national_id: str,
    password: str
):
    user = (
        db.query(User)
        .filter(
            User.national_id == national_id
        )
        .first()
    )

    
    if not user:
        raise ValueError(
            "Invalid national ID or password"
        )
    
    if not user.is_active:
        raise Exception(
            "حساب کاربری شما غیرفعال شده است."
        )

    
    if not verify_password(
        password,
        user.password_hash
    ):
        raise ValueError(
            "Invalid national ID or password"
        )
            
    if not user.is_active:
        raise ValueError(
            "Invalid national ID or password"
        )
    
    return user