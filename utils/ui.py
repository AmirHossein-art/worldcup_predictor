import base64
import streamlit as st
from pathlib import Path

def font_to_base64(font_path):
    with open(font_path, "rb") as font_file:
        return base64.b64encode(
            font_file.read()
        ).decode("utf-8")


def load_main_css():
    css_path = (
        Path("assets")
        / "styles"
        / "main.css"
    )

    regular_font_path = (
        Path("assets")
        /"fonts"
        /"Vazirmatn-Regular.woff2"
    )

    bold_font_path = (
        Path("assets")
        /"fonts"
        /"Vazirmatn-Bold.woff2"
    )

    font_faces = ""

    if regular_font_path.exists():
        regular_font_base64 = font_to_base64(
            regular_font_path
        )

        font_faces += f"""

        @font-face {{
            font-family: "Vazirmatn";
            src: url(data:font/woff2;base64,{regular_font_base64}) format("woff2");
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }}
        """
    
    if bold_font_path.exists():
        bold_font_base64 = font_to_base64(
            bold_font_path
        )

        font_faces += f"""

        @font-face {{
            font-family: "Vazirmatn";
            src: url(data:font/woff2;base64,{regular_font_base64}) format("woff2");
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }}
        """

    css_context = ""

    if css_path.exists():

        css_context = css_path.read_text(
            encoding="utf-8"
        )

        st.markdown(
            f"""
            <style>
            {font_faces}
            {css_context}
            </style>
            """,
            unsafe_allow_html=True
        )
