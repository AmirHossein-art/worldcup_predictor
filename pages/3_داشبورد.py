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


st.button(
    "⚽ پیش‌بینی بازی‌ها",
    use_container_width=True,
    disabled=True
)

st.button(
    "🏆 پیش‌بینی قهرمان",
    use_container_width=True,
    disabled=True
)

st.button(
    "📊 رتبه‌بندی",
    use_container_width=True,
    disabled=True
)