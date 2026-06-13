import streamlit as st
from datetime import datetime

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
from database.models import (
    TournamentPrediction
)

from utils.system_settings import (
    get_system_settings
)

from utils.time_utils import (
    format_shamsi_datetime
)

from config.teams import (
    TEAMS_FLAGS
)

from utils.auth_guard import (
    require_login
)

from utils.constants import (
    SESSION_USER_ID
)

require_login()

st.title(
    "🏆 پیش‌بینی قهرمان جام"
)

st.info(
    """
⚠️ پیش‌بینی قهرمان جام یک‌بار ثبت می‌شود و می‌توانید **قبل از شروع اولین بازی** آن را تغییر دهید.

"""
)

db = SessionLocal()
settings = get_system_settings(db)

existing = (
    db.query(
        TournamentPrediction
    )
    .filter(
        TournamentPrediction.user_id
        ==
        st.session_state[
            SESSION_USER_ID
        ]
    )
    .first()
)

champion_locked = False

if (
    settings.champion_deadline
    and
    datetime.utcnow()
    >=
    settings.champion_deadline
):

    champion_locked = True

if settings.champion_deadline:

    st.info(
        f"⏰ مهلت نهایی انتخاب قهرمان: "
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

        hours = (
            total_seconds % 86400
        ) // 3600

        minutes = (
            total_seconds % 3600
        ) // 60

        st.warning(
            f"⚠️ فقط {days} روز، "
            f"{hours} ساعت و "
            f"{minutes} دقیقه "
            f"تا بسته شدن امکان انتخاب قهرمان باقی مانده است."
        )

team_options = list(
    TEAMS_FLAGS.keys()
)

champion_index = 0

if existing:

    champion_index = (
        team_options.index(
            existing.champion
        )
        if existing.champion
        in team_options
        else 0
    )

if champion_locked:

    st.error(
        "⛔ مهلت انتخاب یا ویرایش قهرمان به پایان رسیده است."
    )

    if existing:

        champion_flag = TEAMS_FLAGS.get(
            existing.champion,
            ""
        )

        st.success(
            f"🏆 انتخاب فعلی شما: "
            f"{champion_flag} "
            f"{existing.champion}"
        )

    else:

        st.info(
            "شما قبل از پایان مهلت، قهرمانی انتخاب نکرده‌اید."
        )

    db.close()

    st.stop()

with st.form(
    "tournament_prediction"
):
    champion = st.selectbox(
        "🏆 قهرمان جام",
        team_options,
        index=champion_index
    )

    submitted = st.form_submit_button(
        "ذخیره پیش‌بینی",
        use_container_width=True
    )

if submitted:
    if existing:

        existing.champion = champion

        db.commit()

        st.success(
            "پیش‌بینی بروزرسانی شد"
        )

        st.rerun()

    else:

        prediction = (
            TournamentPrediction(
                user_id=st.session_state[
                    SESSION_USER_ID
                ],
                champion=champion
            )
        )

        db.add(
            prediction
        )

        db.commit()

        st.success(
            "پیش‌بینی ثبت شد"
        )

        st.rerun()

if existing:

    st.divider()

    st.subheader(
        "پیش‌بینی فعلی شما"
    )

    champion_flag = (
        TEAMS_FLAGS.get(
            existing.champion,
            ""
        )
    )

    st.success(
        f"🏆 {champion_flag} "
        f"{existing.champion}"
    )

db.close()