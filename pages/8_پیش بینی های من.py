import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import Prediction, TournamentPrediction

from config.teams import TEAMS_FLAGS

from utils.auth_guard import require_login
from utils.constants import SESSION_USER_ID

require_login()

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

    champion_flag = TEAMS_FLAGS.get(
        tournament_prediction.champion,
        ""
    )

    st.success(
        f"🥇 قهرمان\n\n"
        f"{champion_flag} {tournament_prediction.champion}"
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

    prediction_rows = []

    for prediction in predictions:

        home_flag = TEAMS_FLAGS.get(
            prediction.match.home_team,
            ""
        )

        away_flag = TEAMS_FLAGS.get(
            prediction.match.away_team,
            ""
        )

        prediction_rows.append(
            {
                "مسابقه": (
                    f"{home_flag} {prediction.match.home_team} "
                    f"VS "
                    f"{away_flag} {prediction.match.away_team}"
                ),
                "پیش‌بینی": (
                    f"{prediction.pred_home} - {prediction.pred_away}"
                ),
                "مرحله": prediction.match.stage,
                "تیم صعود کننده": (
                    prediction.pred_qualified_team
                    if prediction.pred_qualified_team
                    else "-"
                )
            }
        )

    predictions_df = pd.DataFrame(
        prediction_rows
    )

    st.dataframe(
        predictions_df,
        use_container_width=True,
        hide_index=True
    )

db.close()
