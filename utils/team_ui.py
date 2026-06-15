import streamlit as st

from utils.teams import get_flag_path


def show_team_flag(team_name, width=36):
    flag_path = get_flag_path(team_name)

    if (
        flag_path
        and
        flag_path.exists()
    ):

        st.image(
            str(flag_path),
            width=width
        )

    else:

        st.write("")


def show_team_block(team_name, width=36):
    col_flag, col_name = st.columns(
        [1, 5],
        vertical_alignment="center"
    )

    with col_flag:
        show_team_flag(
            team_name,
            width=width
        )

    with col_name:
        st.markdown(
            f"### {team_name}"
        )


def show_team_inline(team_name, width=28):
    col_flag, col_name = st.columns(
        [1, 8],
        vertical_alignment="center"
    )

    with col_flag:
        show_team_flag(
            team_name,
            width=width
        )

    with col_name:
        st.write(team_name)