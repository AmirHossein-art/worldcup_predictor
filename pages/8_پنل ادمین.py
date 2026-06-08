import streamlit as st

from utils.auth_guard import require_login
from utils.constants import ADMIN_NATIONAL_IDS, SESSION_USER_ID

from database.connection import SessionLocal
from database.models import User

require_login()

if st.session_state.get("national_id") not in ADMIN_NATIONAL_IDS:
    st.error("دسترسی غیرمجاز")
    st.stop()

st.title("پنل ادمین - مدیریت کاربران")

db = SessionLocal()

users = db.query(User).all()

for user in users:

    st.write("---")

    st.write(f"نام: {user.first_name} {user.last_name}")
    st.write(f"کد ملی: {user.national_id}")
    st.write(f"معاونت: {user.department}")
    st.write(f"وضعیت: {'تایید شده' if user.is_verified else 'در انتظار'}")

    if not user.is_verified:

        if st.button(
            f"تایید {user.national_id}",
            key=f"verify_{user.user_id}"
        ):

            user.is_verified = True
            db.commit()

            st.success("کاربر تایید شد")
            st.rerun()

db.close()