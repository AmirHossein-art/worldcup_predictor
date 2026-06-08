import streamlit as st

from database.connection import SessionLocal
from database.models import Match, Prediction, Prediction

from config.stages import STAGES
from config.teams import TEAMS_FLAGS

from utils.auth_guard import require_login, require_admin
from utils.constants import SESSION_USER_ID
from utils.constants import SESSION_USER_ID

require_login()

db = SessionLocal()

from datetime import datetime

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
    
with st.container(border=True):

    st.markdown(f"""
    ### {match.home_team} 🆚 {match.away_team}
    """)

if existing:

    st.success(
        f"پیش‌بینی شما: "
        f"{existing.pred_home} - {existing.pred_away}"
    )

    st.stop()

home_pred = st.number_input(
    f"گل {match.home_team}",
    min_value=0,
    step=1,
    key=f"home_{match.match_id}"
)

away_pred = st.number_input(
    f"گل {match.away_team}",
    min_value=0,
    step=1,
    key=f"away_{match.match_id}"
)

if st.button(
    "ثبت پیش‌بینی",
    key=f"submit_{match.match_id}",
    use_container_width=True
):

    new_pred = Prediction(
        user_id=st.session_state[SESSION_USER_ID],
        match_id=match.match_id,
        pred_home=home_pred,
        pred_away=away_pred
    )

    db.add(new_pred)
    db.commit()

    st.success("پیش‌بینی ثبت شد")

    st.rerun()