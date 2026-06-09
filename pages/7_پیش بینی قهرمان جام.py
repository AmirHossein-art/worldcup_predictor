import streamlit as st

from database.connection import SessionLocal
from database.models import (
    TournamentPrediction
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