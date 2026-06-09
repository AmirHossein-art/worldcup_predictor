import streamlit as st

from utils.auth_guard import require_admin, require_login
from utils.constants import ADMIN_NATIONAL_IDS, SESSION_USER_ID

from database.connection import SessionLocal
from database.models import User

require_login()
require_admin()

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
    st.write(f"فعال: {'✅' if user.is_active else '❌'}")

    if user.is_active:
        if st.button(
            f"🚫 غیرفعال کردن {user.national_id}",
            key=f"deactivate_{user.user_id}"
        ):
            user.is_active = False
            db.commit()
            st.rerun()
    else:
        if st.button(
            f"✅ فعال کردن {user.national_id}",
            key=f"activate_{user.user_id}"
        ):
            user.is_active = True
            db.commit()
            st.rerun()


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