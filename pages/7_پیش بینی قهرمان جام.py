import streamlit as st
from datetime import datetime

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

from utils.teams import (
    get_team_names,
    get_flag_path
)

from utils.auth_guard import (
    require_login,
    require_password_change_if_needed
)

from utils.constants import (
    SESSION_USER_ID
)

st.set_page_config(
    page_title="قهرمان جام",
    page_icon="🏆",
    layout="centered",
)

require_login()

require_password_change_if_needed()

load_main_css()

st.title(
    "🏆 پیش‌بینی قهرمان جام"
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

team_options = get_team_names()

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

        st.success(
            f"🏆انتخاب فعلی شما: {existing.champion}"
        )

        existing_flag_path = get_flag_path(
            existing.champion
        )

        if (
            existing_flag_path
            and
            existing_flag_path.exists()
        ):
            st.image(
                str(existing_flag_path),
                width=64
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

    champion_flag_path = get_flag_path(
        champion
    )

    if (
        champion_flag_path
        and
        champion_flag_path.exists()
    ):
        st.image(
            str(champion_flag_path),
            width=56
        )

        st.caption(
            f"تیم انتخاب شده: {champion}"
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

    st.success(
        f"🏆{existing.champion}"
    )

    existing_flag_path = get_flag_path(
        existing.champion
    )

    if (
        existing_flag_path
        and
        existing_flag_path.exists()
    ):
        st.image(
            str(existing_flag_path),
            width=64
        )

db.close()