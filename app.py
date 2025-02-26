import streamlit as st

st.title("Healthcare Translation Web App with Generative AI")

uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])
if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("Transcribe Audio"):
        pass
    # create two drop down menus for the source and target languages
    source_lang = st.selectbox("Select the source language", ["English", "Urdu", "Spanish", "French"])
    target_lang = st.selectbox("Select the target language", ["English", "Urdu", "Spanish", "French"])
    if st.button("Translate transcript"):
        pass