import streamlit as st

from utils.constants import (
    EXACT_SCORE_POINTS,
    WINNER_DIFF_POINTS,
    WINNER_ONLY_POINTS,
    DRAW_ONLY_POINTS,
    QUALIFIED_TEAM_POINTS,
    CHAMPION_POINTS,
)

from utils.auth_guard import require_login

require_login()

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

st.subheader("⚽ امتیازات مسابقات جام جهانی")

with st.expander("🎯 نحوه محاسبه امتیازات", expanded=True):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"✅ **نتیجه دقیق (هم گل‌ها و هم برنده)**\n\n{EXACT_SCORE_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: 2-1\n\nنتیجه واقعی: 2-1 ✓")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"✅ **برنده + تفاضل گل‌ها**\n\n{WINNER_DIFF_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: 2-0\n\nنتیجه واقعی: 3-1 ✓")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning(f"⚠️ **برابری (هر دو تیم)**\n\n{DRAW_ONLY_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: 1-1\n\nنتیجه واقعی: 2-2 ✓")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning(f"⚠️ **فقط برنده صحیح**\n\n{WINNER_ONLY_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: 2-0\n\nنتیجه واقعی: 1-0 ✓")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🏆 **تیم صعودکننده صحیح (فقط در مسابقات برابری و حذفی)**\n\n{QUALIFIED_TEAM_POINTS} امتیاز")
        
    with col2:
        st.info(f"""📊 **مثال:**
        
**در برابری:**
پیش‌بینی برابری: 1-1
نتیجه واقعی: 1-1 ✓
انتخاب صعودکننده: ایران ✓
→ 3 امتیاز

**در برنده معین:**
پیش‌بینی: اسپانیا 2-1 ✓
انتخاب صعودکننده: اسپانیا ✓
→ 3 امتیاز (زیرا برنده شناخته شده)
        """)


# ============================================
# امتیازات قهرمانی
# ============================================

st.subheader("🏆 امتیازات قهرمانی")

with st.expander("🎯 پیش‌بینی قهرمان جام"):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"🥇 **قهرمان درست**\n\n{CHAMPION_POINTS} امتیاز")
        
    with col2:
        st.info(f"📊 **مثال:**\n\nپیش‌بینی: آرژانتین\n\nقهرمان واقعی: آرژانتین ✓")


# ============================================
# خلاصه
# ============================================

st.subheader("📊 خلاصه امتیازات")

scores_data = {
    "📋 نوع": [
        "نتیجه دقیق",
        "برنده + تفاضل",
        "برابری",
        "فقط برنده",
        "تیم صعودکننده",
        "قهرمان جام"
    ],
    "🎯 امتیاز": [
        EXACT_SCORE_POINTS,
        WINNER_DIFF_POINTS,
        DRAW_ONLY_POINTS,
        WINNER_ONLY_POINTS,
        QUALIFIED_TEAM_POINTS,
        CHAMPION_POINTS
    ]
}

st.dataframe(scores_data, use_container_width=True, hide_index=True)

total_possible = (
    EXACT_SCORE_POINTS + 
    CHAMPION_POINTS
)

st.info(
    f"""
    💡 **حداکثر امتیاز در یک مسابقه:**
    
    **برابری:**
    - نتیجه برابری دقیق + صعودکننده درست = {DRAW_ONLY_POINTS} + {QUALIFIED_TEAM_POINTS} = {DRAW_ONLY_POINTS + QUALIFIED_TEAM_POINTS} امتیاز
    
    **برنده معین:**
    - نتیجه دقیق (برنده + تفاضل) + صعودکننده خودکار = {EXACT_SCORE_POINTS} + {QUALIFIED_TEAM_POINTS} = {EXACT_SCORE_POINTS + QUALIFIED_TEAM_POINTS} امتیاز
    
    💡 **حداکثر امتیاز قهرمانی:**
    - پیش‌بینی قهرمان = {CHAMPION_POINTS} امتیاز
    """
)

# ============================================
# قوانین مهم
# ============================================

st.subheader("⚠️ قوانین مهم")

st.warning(
    """
    **شرط اساسی:**
    - 🕒 امتیازدهی **تنها بر اساس نتیجه پایان 90 دقیقه قانونی** انجام می‌شود
    - ⏱️ وقت اضافه و پنالتی در امتیازدهی دخالت ندارند
    - 🔒 پس از شروع بازی، نمی‌توانید پیش‌بینی خود را تغییر دهید
    
    **نکات صعودکننده:**
    - 🏆 اگر نتیجه برابری است: **باید صعودکننده را دستی انتخاب کنید**
    - 🏆 اگر برنده معین است: صعودکننده **خودکار برنده** است (اگر نتیجه درست باشد، صعودکننده هم درست است)
    - ❌ اگر نتیجه برنده شما غلط است، صعودکننده امتیاز نمی‌دهد
    
    **نکات عمومی:**
    - 🎯 هر کاربر می‌تواند برای هر مسابقه **یک بار** پیش‌بینی کند
    - 🔄 می‌توانید پیش‌بینی خود را **قبل از شروع بازی** تغییر دهید
    - 📊 امتیازات **هنگام ورود نتیجه** محاسبه می‌شوند
    """
)

st.divider()

st.success(
    "✅ **اگر سؤالی دارید، با ادمین تماس بگیرید**"
)
