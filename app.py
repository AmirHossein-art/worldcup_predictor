import streamlit as st
from utils.ui import load_main_css
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
        url("data:image/png;base64,{img}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

</style>
""",
unsafe_allow_html=True
)

from utils.constants import (
    EXACT_SCORE_POINTS,
    WINNER_DIFF_POINTS,
    WINNER_ONLY_POINTS,
    QUALIFIED_TEAM_POINTS,
    CHAMPION_POINTS,
)

from utils.ui import load_main_css

st.set_page_config(
    page_title="پیش‌بینی جام جهانی",
    page_icon="⚽",
    layout="centered",
)

load_main_css()

st.title("🏆 مسابقه پیش‌بینی جام جهانی ۲۰۲۶")

st.write(
    "از منوی سمت چپ وارد شوید یا ثبت نام کنید."
)

with st.expander("⚽ امتیازات مسابقات"):
    st.markdown(f"""
    - **نتیجه دقیق:** {EXACT_SCORE_POINTS} امتیاز
    - **نتیجه صحیح + تفاضل گل صحیح:** {WINNER_DIFF_POINTS} امتیاز
    - **نتیجه صحیح (فقط):** {WINNER_ONLY_POINTS} امتیاز
    - **تیم صعودکننده:** {QUALIFIED_TEAM_POINTS} امتیاز (فقط در حذفی)
    """)

#with st.expander("🏆 امتیازات قهرمانی"):
#    st.markdown(f"""
#    - **پیش‌بینی قهرمان درست:** {CHAMPION_POINTS} امتیاز
#    """)

st.info(
    """
    👉 **برای توضیحات کامل تر درباره سیستم امتیازدهی و قوانین مهم، 
    به صفحه «قوانین و امتیازدهی» مراجعه کنید.**
    """
)