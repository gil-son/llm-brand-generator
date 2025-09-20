import streamlit as st
import asyncio
from agent import generate_branding
from pollinations_api import generate_logo_image
from colormagic_api import generate_slogan_palette
from assets import (
    LOGO_BASE64,
    SUGGESTED_NAME,
    SLOGAN_TEXT,
    BRANDING_TEXT,
    SLOGAN_IMAGE,
    PALLETES_IMAGE,
)

if "current_image" not in st.session_state:
    st.session_state.current_image = LOGO_BASE64


def render_title():
    """Render the app title with the current logo image."""
    st.markdown(
        f"""
        <h1 style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{st.session_state.current_image}" 
                 style="height:100px; margin-right:20px;">
            Branding AI Assistant
        </h1>
        """,
        unsafe_allow_html=True,
    )


render_title()
st.write("Create name, slogan, and brand concept from a description.")

description = st.text_area("Describe your brand/business:", height=150)


async def generate_assets(result):
    """Run logo and color palette generation concurrently."""
    logo_task = generate_logo_image(result["logo_mark"])
    palette_task = generate_slogan_palette(
        result["slogan"], query=result["color"].lower()
    )
    slogan_img, (palette_img, palette_text, palette_colors) = await asyncio.gather(
        logo_task, palette_task
    )
    return slogan_img, palette_img, palette_text, palette_colors


if st.button("Generate Branding"):
    if description.strip():
        with st.spinner("Generating..."):
            result = generate_branding(description)
            print("[logo_mark]:", result["logo_mark"])
            print("[color]:", result["color"].lower())

            slogan_img, palette_img, palette_text, palette_colors = asyncio.run(
                generate_assets(result)
            )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{SUGGESTED_NAME}" style="height:50px;">
                    Suggested name:
                </h3>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h2 style='color:#919DC1;'>{result['name']}</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{SLOGAN_TEXT}" style="height:50px;">
                    Suggested slogan:
                </h3>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h3 style='color:#919DC1; font-style:italic;'>{result['slogan']}</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{BRANDING_TEXT}" style="height:50px;">
                    Branding Concept:
                </h3>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='color:#919DC1; font-size:18px; line-height:1.6;'>{result['explanation']}</p>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{SLOGAN_IMAGE}" style="height:50px;">
                    Logo Mark:
                </h3>
                """,
                unsafe_allow_html=True,
            )
            st.image(slogan_img)

            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{PALLETES_IMAGE}" style="height:50px;">
                    Pallete Visual:
                </h3>
                """,
                unsafe_allow_html=True,
            )
            st.image(palette_img)
            st.markdown(f"**Palette name:** {palette_text}")
            st.markdown(f"**Colors:** {', '.join(palette_colors)}")

    else:
        st.warning("Please enter a description before generating.")