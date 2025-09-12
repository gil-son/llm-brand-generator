import streamlit as st
from agent import generate_branding
from pollinations_api import generate_slogan_image
from assets import LOGO_BASE64, SUGGESTED_NAME, SLOGAN_TEXT, BRANDING_TEXT, SLOGAN_IMAGE

if "current_image" not in st.session_state:
    st.session_state.current_image = LOGO_BASE64

def render_title():
    st.markdown(
        f"""
        <h1 style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{st.session_state.current_image}" 
                 style="height:100px; margin-right:20px;">
            Branding AI Assistant
        </h1>
        """,
        unsafe_allow_html=True
    )

render_title()
st.write("Create name, slogan, and brand concept from a description.")

description = st.text_area("Describe your brand/business:", height=150)

if st.button("Generate Branding"):
    #description = "Create something for the Breakfast"
    if description.strip():
        with st.spinner("Generating..."):
            result = generate_branding(description)
            slogan_img = generate_slogan_image(result["slogan"])
        
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{SUGGESTED_NAME}" style="height:50px;">
                    Suggested name:
                </h3>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"<h2 style='color:#919DC1;'>{result['name']}</h2>", unsafe_allow_html=True)   
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{SLOGAN_TEXT}" style="height:50px;">
                    Suggested slogan:
                </h3>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"<h3 style='color:#919DC1; font-style:italic;'>{result['slogan']}</h3>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{BRANDING_TEXT}" style="height:50px;">
                    Branding Concept:
                </h3>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"<p style='color:#919DC1; font-size:18px; line-height:1.6;'>{result['explanation']}</p>", unsafe_allow_html=True)

        with col2:    
            st.markdown(
                f"""
                <h3 style="display:flex; align-items:center; gap:10px;">
                    <img src="data:image/png;base64,{SLOGAN_IMAGE}" style="height:50px;">
                    Slogan Visual:
                </h3>
                """,
                unsafe_allow_html=True
            )
            st.image(slogan_img)
    else:
        st.warning("Please enter a description before generating.")