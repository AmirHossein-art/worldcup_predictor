from utils.auth_guard import (
    require_login
)

require_login()

import streamlit as st

from utils.constants import (
    SESSION_FIRST_NAME,
    SESSION_LAST_NAME,
    SESSION_IS_VERIFIED
)

st.title(
    "🏆 داشبورد"
)

full_name = (
    f"{st.session_state[SESSION_FIRST_NAME]} "
    f"{st.session_state[SESSION_LAST_NAME]}"
)

st.write(
    f"خوش آمدید {full_name}"
)
if not st.session_state[
    SESSION_IS_VERIFIED
]:

    st.warning(
        """
حساب شما هنوز توسط مدیر سامانه تایید نشده است.

شما می‌توانید پیش‌بینی ثبت کنید اما در رتبه‌بندی نمایش داده نخواهید شد.
        """
    )

else:

    st.success(
        "حساب شما تایید شده است."
    )


if st.button(
    "👤 پروفایل من",
    use_container_width=True
):
    st.switch_page(
        "pages/6_پروفایل من.py"
    )

if st.button(
    "⚽ پیش‌بینی مسابقات",
    use_container_width=True
):
    st.switch_page(
        "pages/4_پیش بینی مسابقات.py"
    )

if st.button(
    "🏆 پیش‌بینی قهرمان جام",
    use_container_width=True
):
    st.switch_page(
        "pages/7_ پیش بینی قهرمان جام.py"
    )

if st.button(
    "📊 رتبه‌بندی",
    use_container_width=True
):
    st.switch_page(
        "pages/5_رتبه بندی.py"
    )

if st.button(
    "📋 پیش‌بینی‌های من",
    use_container_width=True
):
    st.switch_page(
        "pages/8_پیش بینی های من.py"
    )

if st.button(
    "📖 قوانین و امتیازدهی",
    use_container_width=True
):
    st.switch_page(
        "pages/9_قوانین و امتیازدهی.py"
    )