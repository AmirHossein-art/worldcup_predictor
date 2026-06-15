import streamlit as st

from streamlit import session_state

from utils.constants import (
    ADMIN_NATIONAL_IDS,
    SESSION_NATIONAL_ID,
    SESSION_MUST_CHANGE_PASSWORD
)


def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


def require_login():

    if not is_logged_in():

        st.warning(
            "ابتدا وارد حساب کاربری شوید."
        )

        st.stop()

def logout():

    keys = list(
        st.session_state.keys()
    )

    for key in keys:

        del st.session_state[key]

def require_admin():

    if (
        st.session_state[
            SESSION_NATIONAL_ID
        ]
        not in ADMIN_NATIONAL_IDS
    ):

        st.error(
            "⛔ دسترسی غیر مجاز"
        )

        st.stop()

def require_password_change_if_needed():
    if st.session_state.get(
        SESSION_MUST_CHANGE_PASSWORD,
        False
    ):
        st.switch_page(
            "pages/22_تغییر رمز عبور.py"
        )