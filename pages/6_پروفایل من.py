from utils.auth_guard import (
    require_login,
    require_password_change_if_needed,
    logout
)

require_login()

require_password_change_if_needed()

import streamlit as st
from utils.ui import load_main_css

from utils.constants import (
    SESSION_FIRST_NAME,
    SESSION_LAST_NAME,
    SESSION_DEPARTMENT,
    SESSION_IS_VERIFIED
)

st.set_page_config(
    page_title="پروفایل من",
    page_icon="👤",
    layout="centered",
)

load_main_css()

st.title(
    "👤 پروفایل من"
    )

full_name = (
    f"{st.session_state[SESSION_FIRST_NAME]} "
    f"{st.session_state[SESSION_LAST_NAME]}"
)

department = st.session_state[
    SESSION_DEPARTMENT
]

st.subheader(
    full_name
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "معاونت",
        department
    )

with col2:

    status = (
        "تایید شده"
        if st.session_state[
            SESSION_IS_VERIFIED
        ]
        else
        "در انتظار تایید"
    )

    st.metric(
        "وضعیت حساب",
        status
    )

if st.button(
    "🏠 بازگشت به داشبورد",
    use_container_width=True
):

    st.switch_page(
        "pages/3_داشبورد.py"
    )



if st.button(
    "🚪 خروج از حساب",
    use_container_width=True
):

    logout()

    st.switch_page(
        "app.py"
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