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
from database.models import Prediction, TournamentPrediction

from utils.teams import (
    get_flag_path
)

from utils.team_ui import(
    show_team_flag,
    show_team_inline
)

from utils.auth_guard import require_login, require_password_change_if_needed
from utils.constants import SESSION_USER_ID

require_login()

require_password_change_if_needed()

st.set_page_config(
    page_title="پیش‌بینی‌های من",
    page_icon="📋",
    layout="centered",
)

load_main_css()

st.title("📋 پیش‌بینی‌های من")

db = SessionLocal()

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
    .filter(
        Prediction.user_id
        ==
        st.session_state[
            SESSION_USER_ID
        ]
    )
    .all()
)

if not predictions:
    st.info("شما هنوز پیش‌بینی ثبت نکرده‌اید")

else:

    for prediction in predictions:
        
        with st.container(border=True):

            match_col1, match_col2, match_col3 = st.columns(
                [4,1,4],
                vertical_alignment="center"
            )

            with match_col1:

                show_team_inline(
                    prediction.match.home_team,
                    width=36
                )

            with match_col2:
                st.markdown(
                    "### VS"
                )

            with match_col3:
               show_team_inline(
                   prediction.match.away_team,
                   width=36
               )

            st.divider()

            info_col1, info_col3 = st.columns(2)
            with info_col1:

                st.metric(
                    "پیش‌بینی شما",
                    f"{prediction.pred_home} - {prediction.pred_away}"
                )

           

            with info_col3:

                qualified_team = prediction.pred_qualified_team or "-"
                
                st.metric(
                    "تیم صعودکننده",
                    qualified_team
                )

                if prediction.pred_qualified_team:

                    show_team_flag(
                        prediction.pred_qualified_team,
                        width=34
                    )
db.close()
