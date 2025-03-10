import streamlit as st
from pages.gemini_api import analyze_symptoms

st.title("🧠 AI Symptom Analysis")

if "body_part" not in st.session_state or "symptoms" not in st.session_state:
    st.error("No symptoms selected. Please go back and enter your symptoms.")
    st.stop()

st.write(f"**Analyzing symptoms for {st.session_state['body_part']}...**")

with st.spinner("Processing your symptoms..."):
    response = analyze_symptoms(st.session_state["body_part"], st.session_state["symptoms"])
    st.session_state["analysis_result"] = response

st.success("Analysis complete! Click below to view results.")

if st.button("View Results"):
    st.switch_page("pages/Results.py")
