import streamlit as st

st.title("📋 AI Health Report")

if "analysis_result" not in st.session_state:
    st.error("No analysis found. Please analyze your symptoms first.")
    st.stop()

st.markdown(st.session_state["analysis_result"])

if st.button("🔄 Check Another Symptom"):
    st.session_state.clear()
    st.switch_page("pages/Symptom_Check.py")
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("./main.py")