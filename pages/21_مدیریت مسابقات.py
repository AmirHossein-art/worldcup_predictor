from datetime import datetime, timedelta

import streamlit as st

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

from database.connection import SessionLocal
from database.models import Match
from utils.system_settings import get_system_settings

from config.stages import STAGES
from config.teams import TEAMS_FLAGS

from utils.auth_guard import require_login, require_admin
from utils.constants import ADMIN_NATIONAL_IDS

from utils.constants import (
    ADMIN_NATIONAL_IDS,
    SESSION_NATIONAL_ID
)

from utils.time_utils import (
    format_shamsi_datetime,
    iran_to_utc,
    utc_to_iran
)


# ==========================
# Auth
# ==========================

require_login()
require_admin()


# ==========================
# Page
# ==========================

st.title("⚽ مدیریت مسابقات")

st.caption(
    "تمام زمان‌ها بر اساس ساعت ایران وارد شوند."
)


# ==========================
# Database Session
# ==========================

db = SessionLocal()
settings = get_system_settings(db)

# ==========================
# Team Options
# ==========================

team_options = list(TEAMS_FLAGS.keys())

# ==========================
# Champion Prediction Lock
# ==========================

st.divider()

st.subheader("🏆 مدیریت پیش‌بینی قهرمان جام")

hours = st.number_input(
    "مهلت بسته شدن از الان، به ساعت",
    min_value=1,
    max_value=168,
    value=24
)

if settings.champion_deadline is None:

    if st.button(
        "🔒 تنظیم مهلت بسته شدن",
        use_container_width=True
    ):

        settings.champion_deadline = (
            datetime.utcnow()
            +
            timedelta(hours=hours)
        )

        db.commit()

        st.success(
            "مهلت بسته شدن پیش‌بینی قهرمان تنظیم شد."
        )

        st.rerun()

else:

    st.info(
        f"⏰ مهلت فعلی: "
        f"{format_shamsi_datetime(settings.champion_deadline)}"
    )

    remaining = (
        settings.champion_deadline
        -
        datetime.utcnow()
    )

    if remaining.total_seconds() > 0:

        total_seconds = int(
            remaining.total_seconds()
        )

        days = total_seconds // 86400

        hours_left = (
            total_seconds % 86400
        ) // 3600

        minutes_left = (
            total_seconds % 3600
        ) // 60

        st.warning(
            f"⏳ {days} روز، "
            f"{hours_left} ساعت و "
            f"{minutes_left} دقیقه "
            f"تا بسته شدن باقی مانده است."
        )

    else:

        st.error(
            "⛔ مهلت پیش‌بینی قهرمان تمام شده است."
        )

    if st.button(
        "🔓 باز کردن دوباره پیش‌بینی قهرمان",
        use_container_width=True
    ):

        settings.champion_deadline = None

        db.commit()

        st.success(
            "پیش‌بینی قهرمان دوباره فعال شد."
        )

        st.rerun()


# ==========================
# Add Match Form
# ==========================

with st.form("add_match_form"):

    st.subheader("➕ افزودن مسابقه")

    col1, col2 = st.columns(2)

    with col1:

        home_team = st.selectbox(
            "تیم میزبان",
            team_options
        )

    with col2:

        away_team = st.selectbox(
            "تیم مهمان",
            team_options
        )

    stage = st.selectbox(
        "مرحله مسابقه",
        STAGES
    )

    kickoff_time = st.datetime_input(
        "زمان شروع مسابقه"
    )

    submitted = st.form_submit_button(
        "ثبت مسابقه",
        use_container_width=True
    )

    if submitted:

        if home_team == away_team:

            st.error(
                "دو تیم نمی‌توانند یکسان باشند"
            )

        else:

            kickoff_time_utc =  iran_to_utc(
                kickoff_time
            )

            new_match = Match(
                home_team=home_team,
                away_team=away_team,
                stage=stage,
                kickoff_time=kickoff_time_utc
            )

            db.add(new_match)

            db.commit()

            st.success(
                "✅ مسابقه با موفقیت ثبت شد"
            )

            st.rerun()


# ==========================
# Matches List
# ==========================

st.divider()

st.subheader("📋 مسابقات ثبت شده")

matches = (
    db.query(Match)
    .order_by(
        Match.kickoff_time
    )
    .all()
)

if not matches:

    st.info(
        "هنوز مسابقه‌ای ثبت نشده است"
    )

else:

    for match in matches:

        action_col1, action_col2 = st.columns(2)

        home_flag = TEAMS_FLAGS.get(
            match.home_team,
            ""
        )

        away_flag = TEAMS_FLAGS.get(
            match.away_team,
            ""
        )

        with st.container(border=True):

            st.markdown(
                f"""
                ### {home_flag} {match.home_team}

                **VS**

                ### {away_flag} {match.away_team}
                """
            )

            st.write(
                f"🏆 {match.stage}"
            )
            
            iran_time = utc_to_iran(
                match.kickoff_time
            )

            st.write(
                f"🕒 {format_shamsi_datetime(match.kickoff_time)}"
            )

            visibility = (
                "🟢 قابل نمایش"
                if match.is_visible
                else
                "🔴 مخفی"
            )

            st.write(
                f"وضعیت: {visibility}"
            )

        with action_col1:

            if match.is_visible:

                if st.button(
                    "🔴 مخفی کردن",
                    key=f"hide_{match.match_id}",
                    use_container_width=True
                ):

                    match.is_visible = False

                    db.commit()

                    st.rerun()

            else:

                if st.button(
                    "🟢 نمایش",
                    key=f"show_{match.match_id}",
                    use_container_width=True
                ):

                    match.is_visible = True

                    db.commit()

                    st.rerun()

        with action_col2:

            if st.button(
                "🗑 حذف",
                key=f"delete_{match.match_id}",
                use_container_width=True
            ):

                db.delete(match)

                db.commit()

                st.success(
                    "مسابقه حذف شد"
                )

                st.rerun()

        if match.result_entered:

            st.success(
                f"نتیجه نهایی: "
                f"{match.home_score}"
                f" - "
                f"{match.away_score}"
            )

        with st.expander(
            "⚽ ثبت نتیجه"
        ):

            home_score = st.number_input(
                f"گل {match.home_team}",
                min_value=0,
                step=1,
                key=f"home_score_{match.match_id}"
            )

            away_score = st.number_input(
                f"گل {match.away_team}",
                min_value=0,
                step=1,
                key=f"away_score_{match.match_id}"
            )

            qualified_team = st.radio(
                "تیم صعود کننده",
                [
                    match.home_team,
                    match.away_team
                ],
                horizontal=True,
                key=f"result_qualified_{match.match_id}"
            )

            if st.button(
                "ثبت نتیجه",
                key=f"save_result_{match.match_id}",
                use_container_width=True
            ):

                match.home_score = home_score

                match.away_score = away_score

                match.qualified_team = qualified_team

                match.result_entered = True

                db.commit()

                st.success(
                    "نتیجه ذخیره شد"
                )

                st.rerun()

db.close()