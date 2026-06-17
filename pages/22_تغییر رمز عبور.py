import streamlit as st
from utils.ui import load_main_css

from database.connection import SessionLocal

from database.models import User

from services.auth_service import hash_password

from utils.auth_guard import require_login

from utils.constants import (
    SESSION_USER_ID,
    SESSION_MUST_CHANGE_PASSWORD
)


require_login()

db = SessionLocal()

user = (
    db.query(User)
    .filter(
        User.user_id
        ==
        st.session_state[
            SESSION_USER_ID
        ]
    )
    .first()
)

if not user:

    db.close()

    st.error(
        "کاربر یافت نشد. لطفاً دوباره وارد شوید."
    )

    st.stop()

if not user.must_change_password:
    db.close()

    st.switch_page(
        "pages/7_پیش بینی قهرمان جام.py"
    )

st.set_page_config(
    page_title="تغییر رمز",
    page_icon="🔐",
    layout="wide",
)

load_main_css()

st.title("🔐 تغییر رمز عبور")

st.warning(
    "برای ادامه استفاده از سامانه، لطفاً رمز عبور خود را تغییر دهید."
)


with st.form("change_password_form"):

    new_password = st.text_input(
        "رمز عبور جدید",
        type="password"
    )

    confirm_password = st.text_input(
        "تکرار رمز عبور جدید",
        type="password"
    )

    submitted = st.form_submit_button(
        "ذخیره رمز جدید",
        use_container_width=True
    )


if submitted:

    if not new_password:

        st.error(
            "رمز عبور جدید را وارد کنید."
        )

    elif len(new_password) < 6:

        st.error(
            "رمز عبور باید حداقل ۶ کاراکتر باشد."
        )

    elif new_password != confirm_password:

        st.error(
            "رمز عبور و تکرار آن یکسان نیستند."
        )

    else:

        user.password_hash = hash_password(
            new_password
        )

        user.must_change_password = False

        db.commit()

        st.session_state[
            SESSION_MUST_CHANGE_PASSWORD
        ] = False

        db.close()

        st.success(
            "رمز عبور با موفقیت تغییر کرد."
        )

        st.switch_page(
            "pages/7_پیش بینی قهرمان جام.py"
        )


db.close()