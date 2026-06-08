import streamlit as st

from config.departments import DEPARTMENTS

from database.connection import SessionLocal

from services.auth_service import (
    register_user
)
from utils.validators import normalize_digits

st.title("ثبت نام")

with st.form("register_form"):

    first_name = st.text_input(
        "نام"
    )

    last_name = st.text_input(
        "نام خانوادگی"
    )

    national_id = st.text_input(
        "کد ملی"
    )

    phone = st.text_input(
        "شماره همراه"
    )

    department = st.selectbox(
        "معاونت",
        DEPARTMENTS
    )

    password = st.text_input(
        "رمز عبور",
        type="password"
    )

    confirm_password = st.text_input(
        "تکرار رمز عبور",
        type="password"
    )

    submit = st.form_submit_button(
        "ثبت نام",
        use_container_width=True
    )

if submit:

    try:

        if password != confirm_password:

            st.error(
                "رمز عبور و تکرار آن یکسان نیست."
            )

        else:

            db = SessionLocal()

            register_user(
                db=db,
                first_name=first_name,
                last_name=last_name,
                national_id=normalize_digits(national_id),
                phone=phone,
                organization="سازمان حمل و نقل و ترافیک",
                department=department,
                password=password
            )

            st.success(
                "ثبت نام با موفقیت انجام شد. پس از تایید ادمین در رتبه‌بندی نمایش داده خواهید شد."
            )

            db.close()

    except Exception as e:

        st.error(str(e))