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

from datetime import datetime

from utils.date_utils import can_predict

from database.connection import SessionLocal
from database.models import Match, Prediction

from utils.team_ui import show_team_html

from utils.auth_guard import require_login, require_password_change_if_needed
from utils.constants import SESSION_USER_ID

from config.stages import KNOCKOUT_STAGES

def get_predicted_qualified_team(
    match,
    home_pred,
    away_pred,
    selected_qualified_team=None
):
    if match.stage not in KNOCKOUT_STAGES:
        return None

    if home_pred > away_pred:
        return match.home_team

    if away_pred > home_pred:
        return match.away_team

    return selected_qualified_team

from utils.time_utils import (
    format_shamsi_datetime,
    iran_to_utc,
    utc_to_iran
)

st.set_page_config(
    page_title="پیش‌بینی مسابقات",
    page_icon="🕶",
    layout="wide",
)

require_login()

require_password_change_if_needed()

db = SessionLocal()

load_main_css()

st.title("⚽ پیش‌بینی مسابقات")

st.info(
    """
⚠️ ثبت پیش‌بینی تا قبل از شروع بازی امکان‌پذیر است.

⚠️ امتیاز نتیجه مسابقه بر اساس نتیجه پایان ۹۰ دقیقه قانونی محاسبه می‌شود.

🏆 در مسابقات حذفی، اگر پیش‌بینی شما مساوی باشد، باید تیم صعودکننده را نیز انتخاب کنید.

👉 **برای توضیحات کامل‌تر درباره سیستم امتیازدهی و قوانین مهم، 
به صفحه «قوانین و امتیازدهی» مراجعه کنید.**
"""
)

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

    if st.session_state.get(
        f"saved_{match.match_id}",
        False
    ):
        st.success(
            "✅ پیش‌بینی ذخیره شد"
        )

        st.session_state[
            f"saved_{match.match_id}"
        ] = False

    existing = (
        db.query(Prediction)
        .filter(
            Prediction.user_id == st.session_state[SESSION_USER_ID],
            Prediction.match_id == match.match_id
        )
        .first()
    )


    with st.container(border=True):

        match_col1, match_col2, match_col3 = st.columns(
            [4,1,4],
            vertical_alignment="center"
        )

        with match_col1:
            show_team_html(
                match.home_team,
                flag_width=58,
                justify="center"
            )

        with match_col2:
            st.markdown(
                "### VS"
            )

        with match_col3:
            show_team_html(
                match.away_team,
                flag_width=58,
                justify="center"
            )

        st.write(
            f"🏆 {match.stage}"
        )

        st.write(
            f"🕒 {format_shamsi_datetime(match.kickoff_time)}"
        )

        prediction_open = can_predict(
            match
        )
        if not prediction_open:
            st.warning(
                "⛔ مهلت ثبت پیش‌بینی به پایان رسیده است"
            )

        st.divider()

        if prediction_open:

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

                selected_qualified_team = None

                if (
                    match.stage in KNOCKOUT_STAGES
                    and
                    home_pred == away_pred
                ):

                    selected_index = 0

                    if existing.pred_qualified_team == match.away_team:
                        selected_index = 1

                    selected_qualified_team = st.radio(
                        "🏆 تیم صعودکننده در صورت مساوی",
                        [
                            match.home_team,
                            match.away_team
                        ],
                        index=selected_index,
                        horizontal=True,
                        key=f"qualified_{match.match_id}"
                    )
                    st.markdown(
                        f"""
                        <div class="qualified-team-caption">
                            🏆 تیم صعودکننده منتخب شما:
                            <strong>{selected_qualified_team}</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif match.stage in KNOCKOUT_STAGES:

                    automatic_qualified_team = get_predicted_qualified_team(
                        match,
                        home_pred,
                        away_pred
                    )

                    st.markdown(
                        f"""
                        <div class="qualified-team-caption">
                            🏆 تیم صعودکننده براساس پیش‌بینی شما:
                            <strong>{automatic_qualified_team}</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if st.button(
                    "💾 ذخیره تغییرات",
                    key=f"update_{match.match_id}",
                    use_container_width=True
                ):

                    existing.pred_home = home_pred
                    existing.pred_away = away_pred
                    existing.pred_qualified_team = get_predicted_qualified_team(
                        match,
                        home_pred,
                        away_pred,
                        selected_qualified_team
                        
                    )

                    db.commit()

                    st.session_state[
                        f"saved_{match.match_id}"
                    ] = True

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

                selected_qualified_team = None

                if (
                    match.stage in KNOCKOUT_STAGES
                    and
                    home_pred == away_pred
                ):

                    selected_qualified_team = st.radio(
                        "🏆 تیم صعودکننده در صورت مساوی",
                        [
                            match.home_team,
                            match.away_team
                        ],
                        horizontal=True,
                        key=f"qualified_{match.match_id}"
                    )
                    st.markdown(
                        f"""
                        <div class="qualified-team-caption">
                            🏆 تیم صعودکننده منتخب شما:
                            <strong>{selected_qualified_team}</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
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
                        pred_qualified_team=get_predicted_qualified_team(
                            match,
                            home_pred,
                            away_pred,
                            selected_qualified_team
                        )
                    )

                    db.add(new_prediction)

                    db.commit()

                    st.session_state[
                        f"saved_{match.match_id}"
                    ] = True

                    st.rerun()

db.close()

