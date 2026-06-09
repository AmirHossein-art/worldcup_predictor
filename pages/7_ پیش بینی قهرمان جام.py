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
runner_up_index = 0

if existing:

    champion_index = (
        team_options.index(
            existing.champion
        )
        if existing.champion
        in team_options
        else 0
    )

    runner_up_index = (
        team_options.index(
            existing.runner_up
        )
        if existing.runner_up
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

    runner_up = st.selectbox(
        "🥈 نایب قهرمان",
        team_options,
        index=runner_up_index
    )

    submitted = st.form_submit_button(
        "ذخیره پیش‌بینی",
        use_container_width=True
    )

if submitted:
    if champion == runner_up:

        st.error(
            "قهرمان و نایب‌قهرمان نمی‌توانند یکسان باشند"
        )

    elif existing:

        existing.champion = champion

        existing.runner_up = runner_up

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
                champion=champion,
                runner_up=runner_up
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

    runner_flag = (
        TEAMS_FLAGS.get(
            existing.runner_up,
            ""
        )
    )

    st.success(
        f"🏆 {champion_flag} "
        f"{existing.champion}"
    )

    st.info(
        f"🥈 {runner_flag} "
        f"{existing.runner_up}"
    )

db.close()