from database.connection import SessionLocal

from services.auth_service import (
    register_user,
    login_user
)

db = SessionLocal()

try:

    user = register_user(
        db=db,
        first_name="Noah",
        last_name="Anderson",
        national_id="1234567890",
        phone="09123456789",
        organization="سازمان حمل و نقل و ترافیک",
        department="معاونت فنی و مهندسی",
        password="123456"
    )

    print(
        f"User created: {user.user_id}"
    )

except Exception as e:

    print(e)

try:

    user = login_user(
        db=db,
        national_id="1234567890",
        password="123456"
    )

    print(
        f"Login successful: {user.first_name}"
    )

except Exception as e:

    print(e)

db.close()