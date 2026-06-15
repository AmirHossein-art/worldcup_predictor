import streamlit as st
from utils.ui import load_main_css

from database.connection import SessionLocal

from services.auth_service import (
    login_user
)

from utils.constants import (
    SESSION_LOGGED_IN,
    SESSION_NATIONAL_ID,
    SESSION_USER_ID,
    SESSION_FIRST_NAME,
    SESSION_LAST_NAME,
    SESSION_DEPARTMENT,
    SESSION_IS_VERIFIED,
    SESSION_MUST_CHANGE_PASSWORD
)
from utils.validators import normalize_digits

st.set_page_config(
    page_title="ورود",
    page_icon="🔑",
    layout="centered",
)

load_main_css()

st.title("ورود")

with st.form("login_form"):

    national_id = st.text_input(
        "کد ملی"
    )

    password = st.text_input(
        "رمز عبور",
        type="password"
    )

    submit = st.form_submit_button(
        "ورود",
        use_container_width=True
    )

if submit:

    try:

        db = SessionLocal()

        user = login_user(
            db=db,
            national_id=normalize_digits(national_id),
            password=password
        )

        st.session_state[
            SESSION_LOGGED_IN
        ] = True

        st.session_state[
            SESSION_USER_ID
        ] = user.user_id

        st.session_state[
            SESSION_FIRST_NAME
        ] = user.first_name

        st.session_state[
            SESSION_LAST_NAME
        ] = user.last_name

        st.session_state[
            SESSION_DEPARTMENT
        ] = user.department

        st.session_state[
            SESSION_IS_VERIFIED
        ] = user.is_verified

        st.session_state[
            SESSION_NATIONAL_ID
        ] = user.national_id

        st.session_state[
            SESSION_MUST_CHANGE_PASSWORD
        ] = user.must_change_password

        st.success(
            "ورود موفقیت‌آمیز بود."
        )

        must_change_password = user.must_change_password

        db.close()

        if must_change_password:
            st.switch_page(
                "pages/22_تغییر رمز عبور.py"
            )

        st.switch_page(
            "pages/7_پیش بینی قهرمان جام.py"
        )

    except Exception as e:

        st.error(
            str(e)
        ) 


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