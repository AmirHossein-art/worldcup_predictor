import streamlit as st

import pandas as pd

from database.connection import SessionLocal
from database.models import StageScoringRule

from utils.ui import load_main_css

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

from utils.constants import (
    EXACT_SCORE_POINTS,
    WINNER_DIFF_POINTS,
    WINNER_ONLY_POINTS,
    QUALIFIED_TEAM_POINTS,
    CHAMPION_POINTS,
)

from utils.auth_guard import require_password_change_if_needed

from utils.stage_display import get_stage_display_name


require_password_change_if_needed()

st.set_page_config(
    page_title="قوانین",
    page_icon="📖",
    layout="wide",
)

load_main_css()

st.title("📖 قوانین و سیستم امتیازدهی")

st.info(
    """
    ⚠️ این صفحه تمام قوانین و نحوه محاسبه امتیازات را شرح می‌دهد.
    
    تمام امتیازات از مقادیر سیستم به صورت **خودکار** به‌روزرسانی می‌شوند.
    """
)

# ============================================
# امتیازات مسابقات
# ============================================

st.subheader("📊 جدول امتیازدهی مراحل")

db = SessionLocal()

try:

    rules = (
        db.query(StageScoringRule)
        .filter(StageScoringRule.is_active == True)
        .order_by(StageScoringRule.rule_id.asc())
        .all()
    )

    if rules:

        rules_data = []
        seen_display_stages = set()

        for rule in rules:

            display_stage = get_stage_display_name(
                rule.stage
            )

            if display_stage in seen_display_stages:
                continue

            seen_display_stages.add(
                display_stage
            )

            max_points = (
                rule.exact_score_points
                +
                rule.qualified_team_points
            )

            rules_data.append(
                {
                    "حداکثر امتیاز": max_points,
                    "تیم صعودکننده": rule.qualified_team_points,
                    "برد / مساوی درست": rule.winner_only_points,
                    "برد + اختلاف گل": rule.winner_diff_points,
                    "نتیجه دقیق": rule.exact_score_points,
                    "مرحله": display_stage,
                }
            )

        st.dataframe(
            pd.DataFrame(rules_data),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("جدول امتیازدهی مراحل هنوز ثبت نشده است.")

finally:

    db.close()

st.subheader("⚽ امتیازات مسابقات جام جهانی")

with st.expander("🎯 نحوه محاسبه امتیازات", expanded=True):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"✅ **نتیجه دقیق (تعداد گل‌های هر دو تیم دقیقاً درست باشد)**\n\n{EXACT_SCORE_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: 2-1\n\nنتیجه واقعی: 2-1 ✓")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"✅ **نتیجه صحیح + تفاضل گل صحیح**\n\n{WINNER_DIFF_POINTS} امتیاز")
        
    with col2:
        st.info(
            f"""📊 **مثال‌ها:**

    **برد:**
    پیش‌بینی: 2-0

    نتیجه واقعی: 3-1 ✓

    **تساوی:**
    پیش‌بینی: 1-1

    نتیجه واقعی: 2-2 ✓
    """
        )
        
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning(f"⚠️ **فقط نتیجه/برنده صحیح**\n\n{WINNER_ONLY_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: 2-0\n\nنتیجه واقعی: 1-0 ✓")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(
            f"""
            🏆 **تیم صعودکننده صحیح در مسابقات حذفی**

            {QUALIFIED_TEAM_POINTS} امتیاز

            این امتیاز فقط برای مسابقات حذفی محاسبه می‌شود.
                    """
        )
        
    with col2:

        rules_html = (
            '<div class="rules-box">'
            '<h4>📊 نحوه تشخیص تیم صعودکننده در پیش‌بینی</h4>'

            '<div class="rule-section-title">'
            'اگر پیش‌بینی شما برنده داشته باشد:'
            '</div>'

            '<p>مثال:</p>'

            '<p>'
            'پیش‌بینی: '
            '<span class="ltr-part">Team A 2 - 1 Team B</span>'
            '</p>'

            '<p>'
            'در این حالت، سیستم '
            '<strong>تیم A</strong> '
            'را به‌عنوان تیم صعودکننده پیش‌بینی‌شده در نظر می‌گیرد.'
            '</p>'

            '<p>اگر تیم A واقعاً صعود کند:</p>'

            f'<p class="score-line">← {QUALIFIED_TEAM_POINTS} امتیاز صعودکننده</p>'

            '<hr>'

            '<div class="rule-section-title">'
            'اگر پیش‌بینی شما مساوی باشد:'
            '</div>'

            '<p>مثال:</p>'

            '<p>'
            'پیش‌بینی: '
            '<span class="ltr-part">Team A 1 - 1 Team B</span>'
            '</p>'

            '<p>'
            'در این حالت باید تیم صعودکننده را جداگانه انتخاب کنید.'
            '</p>'

            '<p>اگر تیم انتخاب‌شده واقعاً صعود کند:</p>'

            f'<p class="score-line">← {QUALIFIED_TEAM_POINTS} امتیاز صعودکننده</p>'

            '</div>'
        )

        st.markdown(
            rules_html,
            unsafe_allow_html=True
        )
# ============================================
# امتیازات قهرمانی
# ============================================

st.subheader("🏆 امتیازات قهرمانی")

with st.expander("🎯 پیش‌بینی قهرمان جام"):
    
    col1, col2 = st.columns(2)
    
    #with col1:
    #    st.success(f"🥇 **قهرمان درست**\n\n{CHAMPION_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: آرژانتین\n\nقهرمان واقعی: آرژانتین ✓")


st.info(
    f"""
💡 **حداکثر امتیاز در یک مسابقه:**

- نتیجه دقیق = {EXACT_SCORE_POINTS} امتیاز
- اگر مسابقه حذفی باشد و تیم صعودکننده نیز درست تشخیص داده شود:
  {EXACT_SCORE_POINTS} + {QUALIFIED_TEAM_POINTS} = {EXACT_SCORE_POINTS + QUALIFIED_TEAM_POINTS} امتیاز

💡 **نکته مهم:**
در مسابقات حذفی، امتیاز تیم صعودکننده جدا از امتیاز نتیجه بازی محاسبه می‌شود.

    """
)

# ============================================
# قوانین مهم
# ============================================

st.subheader("⚠️ قوانین مهم")

st.warning(
    """
**شرط اساسی:**
- 🕒 امتیازدهی نتیجه مسابقه فقط بر اساس نتیجه پایان ۹۰ دقیقه قانونی انجام می‌شود
- ⏱️ وقت اضافه و پنالتی در امتیازدهی نتیجه مسابقه دخالت ندارند
- 🔒 پس از شروع بازی، نمی‌توانید پیش‌بینی خود را تغییر دهید

**نکات مربوط به تیم صعودکننده در مسابقات حذفی:**
- 🏆 امتیاز تیم صعودکننده فقط برای مسابقات حذفی محاسبه می‌شود
- ⚽ اگر پیش‌بینی شما برنده داشته باشد، سیستم همان تیم برنده را به‌عنوان تیم صعودکننده پیش‌بینی‌شده در نظر می‌گیرد
- 🤝 اگر پیش‌بینی شما مساوی باشد، باید تیم صعودکننده را به‌صورت دستی انتخاب کنید
- ✅ اگر تیم صعودکننده پیش‌بینی‌شده با تیم صعودکننده واقعی یکسان باشد، امتیاز صعودکننده را دریافت می‌کنید
- ❌ اگر برد یک تیم را پیش‌بینی کرده باشید، انتخاب دستی صعودکننده نمایش داده نمی‌شود

**مثال‌ها:**
- پیش‌بینی: تیم A 2 - 1 تیم B  
  صعودکننده پیش‌بینی‌شده: تیم A

- پیش‌بینی: تیم A 1 - 1 تیم B  
  در این حالت باید صعودکننده را جداگانه انتخاب کنید

**نکات عمومی:**
- 🎯 هر کاربر می‌تواند برای هر مسابقه یک پیش‌بینی ثبت کند
- 🔄 می‌توانید پیش‌بینی خود را قبل از شروع بازی تغییر دهید
- 📊 امتیازات پس از ورود نتیجه مسابقه محاسبه می‌شوند
    """
)

st.divider()

st.success(
    "✅ **اگر سؤالی دارید، با ادمین تماس بگیرید**"
)
