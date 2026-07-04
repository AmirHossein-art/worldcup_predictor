import streamlit as st
from utils.ui import load_main_css

from services.snapshot_service import save_daily_score_snapshots
from admin_views.scoring_management import render_scoring_management

# Background image
from utils.background import get_base64

img = get_base64("assets/background.png")

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image:
            linear-gradient(
                rgba(0,0,0,0.45),
                rgba(0,0,0,0.45)
            ),
            url("data:image/jpeg;base64,{img}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

from utils.auth_guard import require_admin, require_login, require_password_change_if_needed
from utils.constants import ADMIN_NATIONAL_IDS, SESSION_USER_ID

from database.connection import SessionLocal
from database.models import User
from services.auth_service import hash_password

require_login()
require_admin()
require_password_change_if_needed()

if st.session_state.get("national_id") not in ADMIN_NATIONAL_IDS:
    st.error("دسترسی غیرمجاز")
    st.stop()


st.set_page_config(
    page_title="ادمین",
    page_icon="🔑",
    layout="wide",
)

load_main_css()

admin_section = st.sidebar.radio(
    "پنل مدیریت",
    [
        "مدیریت مسابقات",
        "مدیریت امتیازدهی",
    ]
)

if admin_section == "مدیریت امتیازدهی":

    render_scoring_management()
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

    with st.expander(
        f"ریست رمز عبور{user.first_name}{user.last_name}"
    ):

        new_password = st.text_input(
            "رمز جدید موقت",
            type="password",
            key=f"new_password_{user.user_id}"
        )

        confirm_password = st.text_input(
            "تکرار رمز جدید موقت",
            type="password",
            key=f"confirm_password_{user.user_id}"
        )

        force_change = st.checkbox(
            "کاربر بعد از ورود مجبور به تغییر رمز شود",
            value=True,
            key=f"force_change_{user.user_id}"
        )

        if st.button(
            f"ذخیره رمز جدید برای {user.national_id}",
            key=f"reset_password_{user.user_id}"
        ):
            if not new_password:

                st.error(
                    "رمز موقت را وارد کنید"
                )

            elif len(new_password) < 6:
                st.error(
                    "رمز موقت باید حداقل ۶ کاراکتر باشد"
                )

            elif new_password != confirm_password:
                st.error(
                    "رمز موقت و تکرار آن یکسان نیستند"
                )

            else:

                user.password_hash = hash_password(
                    new_password
                )

                user.must_change_password = force_change

                db.commit()

                st.success(
                    "رمز عبور کاربر با موفقیت ریست شد"
                )

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