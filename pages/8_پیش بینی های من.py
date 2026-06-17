import streamlit as st
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
from database.models import Match, Prediction, TournamentPrediction

from utils.teams import (
    get_flag_path
)

from utils.team_ui import(
    show_team_flag,
    show_team_compact
)

from utils.auth_guard import require_login, require_password_change_if_needed
from utils.constants import SESSION_USER_ID

from services.scoring_service import calculate_prediction_score

require_login()

require_password_change_if_needed()

st.set_page_config(
    page_title="پیش‌بینی‌های من",
    page_icon="📋",
    layout="wide",
)

load_main_css()

st.title("📋 پیش‌بینی‌های من")

db = SessionLocal()

# ==========================
# Helper functions to display
# ==========================

def format_score_with_teams(
    home_team,
    home_score,
    away_score,
    away_team
):
    return (
        f"{home_team}: {home_score} "
        f"| "
        f"{away_team}: {away_score}"
    )


def get_prediction_points_text(
    prediction
):
    match = prediction.match

    if not match.result_entered:
        return "در انتظار نتیجه"

    score = calculate_prediction_score(
        prediction,
        match
    )

    return f"{score} امتیاز"

# ==========================
# Tournament Prediction
# ==========================

tournament_prediction = (
    db.query(TournamentPrediction)
    .filter(
        TournamentPrediction.user_id
        ==
        st.session_state[
            SESSION_USER_ID
        ]
    )
    .first()
)

if tournament_prediction:

    st.subheader("🏆 پیش‌بینی قهرمان جام")

    with st.container(border=True):

        col_flag, col_text = st.columns(
            [1,6],
            vertical_alignment="center"
        )

        with col_flag:

            show_team_flag(
                tournament_prediction.champion,
                width=60
            )

        with col_text:
            st.success(
                f"🥇قهرمان :"
                f"{tournament_prediction.champion}"
            )

    st.divider()

# ==========================
# Match Predictions
# ==========================

st.subheader("⚽ پیش‌بینی‌های بازی‌ها")

predictions = (
    db.query(Prediction)
    .join(Match)
    .filter(
        Prediction.user_id
        ==
        st.session_state[
            SESSION_USER_ID
        ]
    )
    .order_by(
        Match.kickoff_time.desc(),
        Match.match_id.asc()
    )
    .all()
)

if not predictions:
    st.info("شما هنوز پیش‌بینی ثبت نکرده‌اید")

else:

    for prediction in predictions:

        match = prediction.match

        if match.result_entered:

            actual_result = format_score_with_teams(
                match.home_team,
                match.home_score,
                match.away_score,
                match.away_team
            )

        else:

            actual_result = "ثبت نشده"

        user_prediction = format_score_with_teams(
            match.home_team,
            prediction.pred_home,
            prediction.pred_away,
            match.away_team
        )

        prediction_points = get_prediction_points_text(
            prediction
        )

        with st.container(border=True):

            match_col1, match_col2, match_col3 = st.columns(
                [4, 1, 4],
                vertical_alignment="center"
            )

            with match_col1:

                show_team_compact(
                    match.home_team,
                    width=24
                )

            with match_col2:

                st.markdown(
                    "**VS**"
                )

            with match_col3:

                show_team_compact(
                    match.away_team,
                    width=24
                )

            info_col1, info_col2, info_col3, info_col4 = st.columns(
                [3, 3, 2, 2],
                vertical_alignment="center"
            )

            with info_col1:

                st.markdown(
                    f"**پیش‌بینی من:** {user_prediction}"
                )

            with info_col2:

                st.markdown(
                    f"**نتیجه بازی:** {actual_result}"
                )

            with info_col3:

                if match.result_entered:

                    st.markdown(
                        f"""
                        <div style="
                            display: inline-block;
                            padding: 4px 10px;
                            border-radius: 10px;
                            background: rgba(40, 167, 69, 0.18);
                            border: 1px solid rgba(40, 167, 69, 0.45);
                            font-weight: 700;
                            font-size: 0.9rem;
                            white-space: nowrap;
                        ">
                            امتیاز: {prediction_points}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div style="
                            display: inline-block;
                            padding: 4px 10px;
                            border-radius: 10px;
                            background: rgba(255, 193, 7, 0.18);
                            border: 1px solid rgba(255, 193, 7, 0.45);
                            font-weight: 700;
                            font-size: 0.9rem;
                            white-space: nowrap;
                        ">
                            {prediction_points}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with info_col4:

                st.caption(
                    f"مرحله: {match.stage}"
                )
db.close()
