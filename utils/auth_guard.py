import streamlit as st


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