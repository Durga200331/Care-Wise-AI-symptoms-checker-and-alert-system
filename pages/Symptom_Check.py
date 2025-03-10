import streamlit as st

st.title("🔍 Check Your Symptoms")

# Select body part
body_part = st.radio("Choose the affected area:", ["Head", "Chest", "Stomach", "Legs"])

# Symptoms dictionary
symptoms_dict = {
    "Head": ["Headache", "Dizziness", "Blurred Vision"],
    "Chest": ["Chest Pain", "Shortness of Breath", "Coughing"],
    "Stomach": ["Abdominal Pain", "Nausea", "Vomiting"],
    "Legs": ["Swelling", "Pain", "Numbness"]
}

# Select symptoms
symptoms = st.multiselect("Select your symptoms:", symptoms_dict[body_part])

if st.button("Proceed to Analysis"):
    if symptoms:
        st.session_state["body_part"] = body_part
        st.session_state["symptoms"] = symptoms
        st.switch_page("pages/Analyze_Symptoms.py")
    else:
        st.warning("Please select at least one symptom.")
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("./main.py")