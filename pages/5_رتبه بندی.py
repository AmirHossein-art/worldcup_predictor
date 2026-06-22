import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

from utils.ui import load_main_css

from database.connection import SessionLocal
from database.models import User

from utils.auth_guard import require_password_change_if_needed

from services.scoring_service import (
    calculate_user_score
)

from utils.user_helpers import (
    get_user_champion_display
)

from services.snapshot_service import get_daily_phenomenon

# ==========================
# Auth
# ==========================



require_password_change_if_needed()


# ==========================
# Page
# ==========================

st.set_page_config(
    page_title="رتبه‌بندی",
    page_icon="🧮",
    layout="wide",
)

load_main_css()

st.title("🏆 رتبه‌بندی کاربران")

st.info(
    """
امتیازات بر اساس میزان دقت پیش‌بینی شما محاسبه می‌شود.

"""
)


# ==========================
# Deputy Comparing def
# ==========================

def build_department_stats(
    all_users_scores
):
    department_stats = {}

    for item in all_users_scores:

        user = item["user"]
        score = item["score"]

        department = (
            user.department
            if user.department
            else "نامشخص"
        )

        if department not in department_stats:

            department_stats[department] = {
                "members_count": 0,
                "scored_members_count": 0,
                "total_score": 0,
                "scored_total_score": 0,
                "max_score": 0,
            }

        department_stats[
            department
        ]["members_count"] += 1

        department_stats[
            department
        ]["total_score"] += score

        if score > 0:

            department_stats[
                department
            ]["scored_members_count"] += 1

            department_stats[
                department
            ]["scored_total_score"] += score

        if score > department_stats[department]["max_score"]:

            department_stats[
                department
            ]["max_score"] = score

    department_rows = []

    for department, stats in department_stats.items():

        members_count = stats["members_count"]
        scored_members_count = stats["scored_members_count"]

        average_all = 0

        if members_count > 0:

            average_all = (
                stats["total_score"]
                /
                members_count
            )

        average_scored = 0

        if scored_members_count > 0:

            average_scored = (
                stats["scored_total_score"]
                /
                scored_members_count
            )

        department_rows.append(
            {
                "معاونت": department,
                "افراد امتیازدار": scored_members_count,
                "میانگین امتیازدارها": round(
                    average_scored,
                    2
                ),
                "بیشترین امتیاز": stats["max_score"],
                "مجموع امتیاز": stats["total_score"],
            }
        )

    department_rows.sort(
        key=lambda row: (
            row["مجموع امتیاز"],
        ),
        reverse=True
    )

    return department_rows

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

    styled_ranking_df = (
        ranking_df
        .style
        .set_properties(
            **{
                "text-align": "center",
                "font-family": "Vazirmatn, Tahoma, Arial, sans-serif",
                "font-size": "16px",
                "font-weight": "600",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("text-align", "center"),
                        ("font-family", "Vazirmatn, Tahoma, Arial, sans-serif"),
                        ("font-size", "16px"),
                        ("font-weight", "800"),
                    ],
                }
            ]
        )
    )

    st.dataframe(
        styled_ranking_df,
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
# Daily Phenomenons
# ==========================

daily_phenomenons = get_daily_phenomenon(
    db
)

if daily_phenomenons:


    st.subheader("🌟 پدیده‌های روز")

    top_daily_phenomenons = daily_phenomenons[:3]

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    medal_titles = [
        "پدیده اول روز",
        "پدیده دوم روز",
        "پدیده سوم روز"
    ]

    columns = st.columns(
        len(top_daily_phenomenons)
    )

    for index, item in enumerate(
        top_daily_phenomenons
    ):

        user = item["user"]

        full_name = (
            f"{user.first_name} "
            f"{user.last_name}"
        )

        with columns[index]:

            st.metric(
                label=(
                    f"{medals[index]} "
                    f"{medal_titles[index]}"
                ),
                value=full_name,
                delta=(
                    f"+{item['score_delta']} امتیاز"
                )
            )

            st.markdown(
                f"""
                <div class="daily-phenomenon-caption">
                    امتیاز فعلی: {item["current_score"]}
                </div>
                """,
                unsafe_allow_html=True
            )


else:

    st.info(
        "امروز هنوز افزایش امتیاز قابل توجهی ثبت نشده است."
    )



# ==========================
# Department Comparison
# ==========================

st.subheader("🏢 رتبه‌بندی بخش‌ها")

department_rows = build_department_stats(
    all_users_scores
)

if department_rows:

    department_df = pd.DataFrame(
        department_rows
    )

    department_df = department_df[
            department_df["افراد امتیازدار"] > 0
    ]

    st.dataframe(
        department_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div class="chart-caption">
            رتبه‌بندی بخش‌ها براساس میانگین افراد امتیازدار
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "هنوز داده‌ای برای مقایسه معاونت‌ها وجود ندارد."
    )

chart_df = department_df[
    [
        "معاونت",
        "میانگین امتیازدارها"
    ]
].copy()

chart_height = max(
    350,
    len(chart_df) * 55
)

department_chart = (
    alt.Chart(chart_df)
    .mark_bar(
        cornerRadiusEnd=6
    )
    .encode(
        x=alt.X(
            "میانگین امتیازدارها:Q",
            title="میانگین امتیاز"
        ),
        y=alt.Y(
            "معاونت:N",
            sort="-x",
            title=None,
            axis=alt.Axis(
                labelLimit=500,
                labelFontSize=14,
                labelPadding=10
            )
        ),
        tooltip=[
            alt.Tooltip(
                "معاونت:N",
                title="معاونت"
            ),
            alt.Tooltip(
                "میانگین امتیازدارها:Q",
                title="میانگین امتیازدارها",
                format=".2f"
            )
        ]
    )
    .properties(
        height=chart_height
    )
)

st.altair_chart(
    department_chart,
    use_container_width=True
)
    

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