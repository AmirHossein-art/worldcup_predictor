import streamlit as st

from datetime import datetime

from database.connection import SessionLocal
from database.models import Match, Prediction

from config.teams import TEAMS_FLAGS

from utils.auth_guard import require_login
from utils.constants import SESSION_USER_ID

from config.stages import KNOCKOUT_STAGES

require_login()

db = SessionLocal()

st.title("⚽ پیش‌بینی مسابقات")


matches = (
    db.query(Match)
    .filter(
        Match.is_visible == True,
        Match.kickoff_time > datetime.utcnow()
    )
    .order_by(Match.kickoff_time)
    .all()
)

if not matches:
    st.info("هیچ مسابقه قابل پیش‌بینی وجود ندارد")
    st.stop()


for match in matches:

    existing = (
        db.query(Prediction)
        .filter(
            Prediction.user_id == st.session_state[SESSION_USER_ID],
            Prediction.match_id == match.match_id
        )
        .first()
    )

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

        st.write(
            f"🕒 {match.kickoff_time}"
        )

        st.divider()

        if existing:

            home_pred = st.number_input(
            f"گل {match.home_team}",
            min_value=0,
            value=existing.pred_home,
            key=f"home_{match.match_id}"
            )

            away_pred = st.number_input(
                f"گل {match.away_team}",
                min_value=0,
                value=existing.pred_away,
                key=f"away_{match.match_id}"
            )

            pred_qualified_team = None

            if match.stage in KNOCKOUT_STAGES:

                selected_index = 0

                if (
                    existing.pred_qualified_team
                    ==
                    match.away_team
                ):
                    selected_index = 1

                pred_qualified_team = st.radio(
                    "🏆 تیم صعود کننده",
                    [
                        match.home_team,
                        match.away_team
                    ],
                    index=selected_index,
                    horizontal=True,
                    key=f"qualified_{match.match_id}"
                )

            if st.button(
                "💾 ذخیره تغییرات",
                key=f"update_{match.match_id}",
                use_container_width=True
            ):

                existing.pred_home = home_pred
                existing.pred_away = away_pred
                existing.pred_qualified_team = pred_qualified_team

                db.commit()

                st.success("تغییرات ذخیره شد")

                st.rerun()

        else:

            col1, col2 = st.columns(2)

            with col1:

                home_pred = st.number_input(
                    f"گل {match.home_team}",
                    min_value=0,
                    step=1,
                    key=f"home_{match.match_id}"
                )

            with col2:

                away_pred = st.number_input(
                    f"گل {match.away_team}",
                    min_value=0,
                    step=1,
                    key=f"away_{match.match_id}"
                )

                pred_qualified_team = None

                if match.stage in KNOCKOUT_STAGES:

                    pred_qualified_team = st.radio(
                        "🏆 تیم صعود کننده",
                        [
                            match.home_team,
                            match.away_team
                        ],
                        horizontal=True,
                        key=f"qualified_{match.match_id}"
                    )
                if st.button(
                    "✅ ثبت پیش‌بینی",
                    key=f"submit_{match.match_id}",
                    use_container_width=True
                ):

                    new_prediction = Prediction(
                        user_id=st.session_state[
                            SESSION_USER_ID
                        ],
                        match_id=match.match_id,
                        pred_home=home_pred,
                        pred_away=away_pred,
                        pred_qualified_team=pred_qualified_team
                    )

                    db.add(new_prediction)

                    db.commit()

                    st.success(
                        "پیش‌بینی ثبت شد"
                    )

                    st.rerun()           

                new_prediction = Prediction(
                    user_id=st.session_state[
                        SESSION_USER_ID
                    ],
                    match_id=match.match_id,
                    pred_home=home_pred,
                    pred_away=away_pred,
                    pred_qualified_team=pred_qualified_team
                )

                db.add(
                    new_prediction
                )

                db.commit()

                st.success(
                    "✅ پیش‌بینی ثبت شد"
                )

                st.rerun()

db.close()