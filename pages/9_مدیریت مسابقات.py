from datetime import datetime

import streamlit as st

from database.connection import SessionLocal
from database.models import Match

from config.stages import STAGES
from config.teams import TEAMS_FLAGS

from utils.auth_guard import require_login, require_admin
from utils.constants import ADMIN_NATIONAL_IDS

from utils.constants import (
    ADMIN_NATIONAL_IDS,
    SESSION_NATIONAL_ID
)


# ==========================
# Auth
# ==========================

require_login()
require_admin()


# ==========================
# Page
# ==========================

st.title("⚽ مدیریت مسابقات")


# ==========================
# Database Session
# ==========================

db = SessionLocal()


# ==========================
# Team Options
# ==========================

team_options = list(TEAMS_FLAGS.keys())


# ==========================
# Add Match Form
# ==========================

with st.form("add_match_form"):

    st.subheader("➕ افزودن مسابقه")

    col1, col2 = st.columns(2)

    with col1:

        home_team = st.selectbox(
            "تیم میزبان",
            team_options
        )

    with col2:

        away_team = st.selectbox(
            "تیم مهمان",
            team_options
        )

    stage = st.selectbox(
        "مرحله مسابقه",
        STAGES
    )

    kickoff_time = st.datetime_input(
        "زمان شروع مسابقه"
    )

    submitted = st.form_submit_button(
        "ثبت مسابقه",
        use_container_width=True
    )

    if submitted:

        if home_team == away_team:

            st.error(
                "دو تیم نمی‌توانند یکسان باشند"
            )

        else:

            new_match = Match(
                home_team=home_team,
                away_team=away_team,
                stage=stage,
                kickoff_time=kickoff_time
            )

            db.add(new_match)

            db.commit()

            st.success(
                "✅ مسابقه با موفقیت ثبت شد"
            )

            st.rerun()


# ==========================
# Matches List
# ==========================

st.divider()

st.subheader("📋 مسابقات ثبت شده")

matches = (
    db.query(Match)
    .order_by(
        Match.kickoff_time
    )
    .all()
)

if not matches:

    st.info(
        "هنوز مسابقه‌ای ثبت نشده است"
    )

else:

    for match in matches:

        action_col1, action_col2 = st.columns(2)

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

            visibility = (
                "🟢 قابل نمایش"
                if match.is_visible
                else
                "🔴 مخفی"
            )

            st.write(
                f"وضعیت: {visibility}"
            )

        with action_col1:

            if match.is_visible:

                if st.button(
                    "🔴 مخفی کردن",
                    key=f"hide_{match.match_id}",
                    use_container_width=True
                ):

                    match.is_visible = False

                    db.commit()

                    st.rerun()

            else:

                if st.button(
                    "🟢 نمایش",
                    key=f"show_{match.match_id}",
                    use_container_width=True
                ):

                    match.is_visible = True

                    db.commit()

                    st.rerun()

        with action_col2:

            if st.button(
                "🗑 حذف",
                key=f"delete_{match.match_id}",
                use_container_width=True
            ):

                db.delete(match)

                db.commit()

                st.success(
                    "مسابقه حذف شد"
                )

                st.rerun()

        if match.result_entered:

            st.success(
                f"نتیجه نهایی: "
                f"{match.home_score}"
                f" - "
                f"{match.away_score}"
            )

        with st.expander(
            "⚽ ثبت نتیجه"
        ):

            home_score = st.number_input(
                f"گل {match.home_team}",
                min_value=0,
                step=1,
                key=f"home_score_{match.match_id}"
            )

            away_score = st.number_input(
                f"گل {match.away_team}",
                min_value=0,
                step=1,
                key=f"away_score_{match.match_id}"
            )

            if st.button(
                "ثبت نتیجه",
                key=f"save_result_{match.match_id}",
                use_container_width=True
            ):

                match.home_score = home_score

                match.away_score = away_score

                match.result_entered = True

                db.commit()

                st.success(
                    "نتیجه ذخیره شد"
                )

                st.rerun()

db.close()