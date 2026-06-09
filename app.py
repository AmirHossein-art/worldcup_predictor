import streamlit as st

from utils.constants import (
    EXACT_SCORE_POINTS,
    WINNER_DIFF_POINTS,
    WINNER_ONLY_POINTS,
    DRAW_ONLY_POINTS,
    QUALIFIED_TEAM_POINTS,
    CHAMPION_POINTS,
)

st.set_page_config(
    page_title="World Cup Predictor",
    page_icon="⚽",
    layout="centered",
)

st.title("🏆 مسابقه پیش‌بینی جام جهانی 2026")

st.write(
    "از منوی سمت چپ وارد شوید یا ثبت نام کنید."
)

with st.expander("⚽ امتیازات مسابقات"):
    st.markdown(f"""
    - **نتیجه دقیق:** {EXACT_SCORE_POINTS} امتیاز
    - **تیم برنده + تفاضل گل:** {WINNER_DIFF_POINTS} امتیاز
    - **برابری:** {DRAW_ONLY_POINTS} امتیاز
    - **تیم برنده:** {WINNER_ONLY_POINTS} امتیاز
    - **تیم صعودکننده:** {QUALIFIED_TEAM_POINTS} امتیاز
    """)

with st.expander("🏆 امتیازات قهرمانی"):
    st.markdown(f"""
    - **پیش‌بینی قهرمان درست:** {CHAMPION_POINTS} امتیاز
    """)