import streamlit as st
import pandas as pd
import plotly.express as px

from utils.ui import load_main_css

from database.connection import SessionLocal
from database.models import User

from utils.auth_guard import require_login, require_password_change_if_needed

from services.scoring_service import (
    calculate_user_score
)

from utils.user_helpers import (
    get_user_champion_display
)

# ==========================
# Auth
# ==========================

require_login()

require_password_change_if_needed()

# ==========================
# Page
# ==========================

st.set_page_config(
    page_title="رتبه‌بندی",
    page_icon="🧮",
    layout="centered",
)

load_main_css()

st.title("🏆 رتبه‌بندی کاربران")

st.info(
    """
امتیازات بر اساس میزان دقت پیش‌بینی شما محاسبه می‌شود.

"""
)

# ==========================
# Database
# ==========================

db = SessionLocal()

# ==========================
# Load Users
# ==========================

users = (
    db.query(User)
    .filter(
        User.is_verified == True,
        User.is_active == True
    )
    .all()
)

all_users_scores = []

for user in users:

    score = calculate_user_score(
        user
    )

    all_users_scores.append(
        {
            "user": user,
            "score": score
        }
    )

# فقط کاربرانی که امتیاز گرفته اند
leaderboard = [
    item
    for item in all_users_scores
    if item["score"] > 0
]

# ==========================
# Sort Leaderboard
# ==========================

leaderboard.sort(
    key=lambda x: x["score"],
    reverse=True
)

# ==========================
# Asign Ranks With Ties
# ==========================

last_score = None
current_rank = 0

for index, item in enumerate(
    leaderboard,
    start=1
):
    if item["score"] != last_score:

        current_rank = index
        last_score = item["score"]
    
    item["rank"] = current_rank


# ==========================
# Build DataFrame
# ==========================

leaderboard_rows = []

for item in leaderboard:

    user = item["user"]

    leaderboard_rows.append(
        {
            "رتبه": item["rank"],
            "نام": (
                f"{user.first_name} "
                f"{user.last_name}"
            ),
            "معاونت": user.department,
            "🏆 قهرمان": get_user_champion_display(user),
            "امتیاز": item["score"]
        }
    )

# ==========================
# Full Ranking Table
# ==========================

st.subheader("📊 جدول رتبه‌بندی")

if leaderboard_rows:

    ranking_df = pd.DataFrame(
        leaderboard_rows
    )

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )

else:

    if users:
        st.info(
            "هنوز هیچ کاربری امتیاز نگرفته است. رتبه‌بندی بعد از ثبت نتایج مسابقات نمایش داده می شود."
        )

    else:

        st.info(
            "هنوز کاربر تایید شده‌ای وجود ندارد."
        )


    

# ==========================
# Top 3 Users
# ==========================

if leaderboard:

    st.subheader(
        "🏅 برترین کاربران"
    )

    top_users = [
        item
        for item in leaderboard
        if item["rank"] <= 3
    ]

    columns = st.columns(
        len(top_users)
    )

    medals = {
        1: "🥇 نفر اول",
        2: "🥈 نفر دوم",
        3: "🥉 نفر سوم"
    }

    for index, item in enumerate(
        top_users
    ):

        user = item["user"]

        with columns[index]:

            st.metric(
                medals.get(
                    item["rank"],
                    f"رتبه {item["rank"]}"
                ),
                (
                    f"{user.first_name}"
                    f"{user.last_name}"
                ),
                item["score"]
            )

    # ==========================
    # Chart
    # ==========================

    chart_rows = []

    for item in top_users:

        user = item["user"]

        chart_rows.append(
            {
                "نام": (
                    f"{user.first_name} "
                    f"{user.last_name}"
                ),
                "امتیاز": item["score"]
            }
        )

    chart_df = (
        pd.DataFrame(
            chart_rows
        )
        .set_index("نام")
    )

    st.subheader(
        "📈 مقایسه امتیاز نفرات برتر"
    )

    fig = px.bar(
        chart_df.reset_index(),
        x="امتیاز",
        y="نام",
        orientation="h",
        labels={"امتیاز": "امتیاز", "نام": "نام"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Close DB
# ==========================

db.close()

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