import streamlit as st
import base64

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

def show_team_compact(team_name, width=24):
    col_flag, col_name = st.columns(
        [1, 7],
        vertical_alignment="center"
    )

    with col_flag:
        show_team_flag(
            team_name,
            width=width
        )

    with col_name:
        st.markdown(
            f"**{team_name}**"
        )

# Keep Flag and Team Name Close Together in a Single Line, with Flag on the Left and Team Name on the Right

def get_flag_base64(team_name):
    flag_path = get_flag_path(
        team_name
    )

    if (
        not flag_path
        or
        not flag_path.exists()
    ):
        return ""

    with open(flag_path, "rb") as file:
        return base64.b64encode(
            file.read()
        ).decode("utf-8")


def show_team_html(
    team_name,
    flag_width=58,
    justify="center"
):
    flag_base64 = get_flag_base64(
        team_name
    )

    if flag_base64:

        flag_html = (
            f'<img '
            f'src="data:image/svg+xml;base64,{flag_base64}" '
            f'style="'
            f'width:{flag_width}px; '
            f'height:auto; '
            f'border-radius:8px; '
            f'display:inline-block; '
            f'flex-shrink:0;'
            f'" '
            f'/>'
        )

    else:

        flag_html = ""

    html = (
        f'<div class="team-line" style="justify-content:{justify};">'
        f'{flag_html}'
        f'<span class="team-name">{team_name}</span>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

# =================================
# Prediction Cards adjustments def
# =================================

def show_prediction_team_html(
    team_name,
    flag_width=34,
    justify="center"
):
    flag_base64 = get_flag_base64(
        team_name
    )

    if flag_base64:

        flag_html = (
            f'<img '
            f'src="data:image/svg+xml;base64,{flag_base64}" '
            f'style="'
            f'width:{flag_width}px; '
            f'height:auto; '
            f'border-radius:6px; '
            f'display:inline-block; '
            f'flex-shrink:0;'
            f'" '
            f'/>'
        )

    else:

        flag_html = ""

    html = (
        f'<div class="prediction-team-line" style="justify-content:{justify};">'
        f'{flag_html}'
        f'<span class="prediction-team-name">{team_name}</span>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )