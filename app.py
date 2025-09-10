import streamlit as st
from agent import generate_branding
from craiyon_api import generate_slogan_image  # arquivo com a função acima

st.title("🤖 Branding AI Assistant")
st.write("Create name, slogan, and brand concept from a description.")

description = st.text_area("Describe your brand/business:", height=150)

if st.button("Generate Branding"):
    if description.strip():
        with st.spinner("Generating..."):
            result = generate_branding(description)
            slogan_img = generate_slogan_image(result["slogan"])
        
        st.subheader("✨ Suggested name:")
        st.write(result["name"])
        st.subheader("💡 Suggested slogan:")
        st.write(result["slogan"])
        st.subheader("📖 Context used (insights from docs):")
        st.write(result["context"])
        st.subheader("🖼 Slogan Visual:")
        st.image(slogan_img)
    else:
        st.warning("Please enter a description before generating.")