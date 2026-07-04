import streamlit as st
import pandas as pd

from database.connection     import SessionLocal
from database.models import StageScoringRule
from config.stages import STAGES

from utils.stage_display import get_stage_display_name


def render_scoring_management():

    st.subheader("⚙️ مدیریت امتیازدهی مراحل")

    if st.session_state.get("stage_scoring_success_message"):

        st.success(
                st.session_state["stage_scoring_success_message"]
        )

        st.session_state["stage_scoring_success_message"] = None

    db = SessionLocal()

    try:

        st.markdown("### 📊 قوانین فعلی امتیازدهی")

        rules = (
            db.query(StageScoringRule)
            .order_by(StageScoringRule.rule_id.asc())
            .all()
        )

        if rules:

            rules_data = []

            for rule in rules:

                max_points = (
                    rule.exact_score_points
                    +
                    rule.qualified_team_points
                )

                display_stage = get_stage_display_name(
                    rule.stage
                )

                rules_data.append(
                    {
                        "مرحله": rule.stage,
                        "مرحله ذخیره‌شده": rule.stage,
                        "نتیجه دقیق": rule.exact_score_points,
                        "برد + اختلاف گل": rule.winner_diff_points,
                        "برد / مساوی درست": rule.winner_only_points,
                        "تیم صعودکننده": rule.qualified_team_points,
                        "حداکثر امتیاز": max_points,
                        "فعال": "بله" if rule.is_active else "خیر",
                    }
                )

            st.dataframe(
                pd.DataFrame(rules_data),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("هنوز قانونی برای امتیازدهی ثبت نشده است.")

        st.divider()

        st.markdown("### ➕ افزودن قانون جدید برای مرحله")

        existing_stages = [
            rule.stage
            for rule in rules
        ]

        available_stages = [
            stage
            for stage in STAGES
            if stage not in existing_stages
        ]

        add_mode = st.radio(
            "نوع مرحله",
            [
                "انتخاب از مراحل موجود",
                "وارد کردن دستی مرحله"
            ],
            horizontal=True
        )

        with st.form("add_stage_scoring_rule_form"):

            if add_mode == "انتخاب از مراحل موجود":

                if available_stages:

                    stage = st.selectbox(
                        "مرحله",
                        available_stages
                    )

                else:

                    stage = None
                    st.info("برای همه مراحل موجود، قانون امتیازدهی ثبت شده است.")

            else:

                stage = st.text_input(
                    "نام مرحله",
                    placeholder="مثلاً 1/4 نهایی"
                )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                exact_score_points = st.number_input(
                    "نتیجه دقیق",
                    min_value=0,
                    step=1,
                    value=12
                )

            with col2:

                winner_diff_points = st.number_input(
                    "برد + اختلاف گل",
                    min_value=0,
                    step=1,
                    value=8
                )

            with col3:

                winner_only_points = st.number_input(
                    "برد / مساوی درست",
                    min_value=0,
                    step=1,
                    value=4
                )

            with col4:

                qualified_team_points = st.number_input(
                    "تیم صعودکننده",
                    min_value=0,
                    step=1,
                    value=3
                )

            submitted = st.form_submit_button(
                "ثبت قانون جدید"
            )

            if submitted:

                if not stage:

                    st.error("نام مرحله را وارد یا انتخاب کنید.")

                else:

                    existing_rule = (
                        db.query(StageScoringRule)
                        .filter(StageScoringRule.stage == stage)
                        .first()
                    )

                    if existing_rule:

                        st.error("برای این مرحله قبلاً قانون امتیازدهی ثبت شده است.")

                    else:

                        new_rule = StageScoringRule(
                            stage=stage,
                            exact_score_points=exact_score_points,
                            winner_diff_points=winner_diff_points,
                            winner_only_points=winner_only_points,
                            qualified_team_points=qualified_team_points,
                            is_active=True
                        )

                        db.add(new_rule)
                        db.commit()

                        st.session_state["stage_scoring_success_message"] = (
                            f"قانون امتیازدهی مرحله «{stage}» با موفقیت ثبت شد."
                        )
                        st.rerun()

        st.divider()

        st.markdown("### ✏️ ویرایش قوانین موجود")

        for rule in rules:

            with st.expander(f"ویرایش {rule.stage}"):

                with st.form(f"edit_rule_{rule.rule_id}"):

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        exact_score_points = st.number_input(
                            "نتیجه دقیق",
                            min_value=0,
                            step=1,
                            value=rule.exact_score_points,
                            key=f"exact_{rule.rule_id}"
                        )

                    with col2:

                        winner_diff_points = st.number_input(
                            "برد + اختلاف گل",
                            min_value=0,
                            step=1,
                            value=rule.winner_diff_points,
                            key=f"diff_{rule.rule_id}"
                        )

                    with col3:

                        winner_only_points = st.number_input(
                            "برد / مساوی درست",
                            min_value=0,
                            step=1,
                            value=rule.winner_only_points,
                            key=f"winner_{rule.rule_id}"
                        )

                    with col4:

                        qualified_team_points = st.number_input(
                            "تیم صعودکننده",
                            min_value=0,
                            step=1,
                            value=rule.qualified_team_points,
                            key=f"qualified_{rule.rule_id}"
                        )

                    is_active = st.checkbox(
                        "فعال باشد",
                        value=rule.is_active,
                        key=f"active_{rule.rule_id}"
                    )

                    submitted = st.form_submit_button(
                        "ذخیره تغییرات"
                    )

                    if submitted:

                        rule.exact_score_points = exact_score_points
                        rule.winner_diff_points = winner_diff_points
                        rule.winner_only_points = winner_only_points
                        rule.qualified_team_points = qualified_team_points
                        rule.is_active = is_active

                        db.commit()

                        st.session_state["stage_scoring_success_message"] = (
                            f"تغییرات امتیازدهی مرحله «{rule.stage}» با موفقیت ذخیره شد."
                        )
                        st.rerun()

    finally:

        db.close()