import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, messaging
import geocoder

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("L:\\hackacthon project\\raj\\hackathonaisymptom-firebase-adminsdk-fbsvc-1271146ca1.json")
    firebase_admin.initialize_app(cred)

st.title("🚨 Emergency Alert System")

# Ensure contacts are loaded from session state
if "emergency_contacts" not in st.session_state or not st.session_state.emergency_contacts:
    st.error("⚠️ No emergency contacts found! Please add them in the main app.")
    st.stop()

if "user_phone" not in st.session_state:
    st.session_state.user_phone = st.session_state.emergency_contacts[0]["User"]  # Set a default

user_phone = st.session_state.user_phone
emergency_contacts = st.session_state.emergency_contacts

st.write(f"⚡ Sending emergency alert from **{user_phone}**")

# Countdown Timer Before Sending Alert
if "alert_triggered" in st.session_state and st.session_state.alert_triggered:
    countdown = 30  # Set countdown to 5 seconds
    countdown_placeholder = st.empty()
    cancel_button_placeholder = st.empty()

    for i in range(countdown, 0, -1):
        countdown_placeholder.markdown(f"<h1 style='text-align: center; color: red;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(1)

        # Allow canceling the alert at any time
        if cancel_button_placeholder.button("❌ Cancel Alert", key=f"cancel_{i}"):
            st.session_state.alert_triggered = False
            countdown_placeholder.empty()
            cancel_button_placeholder.empty()
            st.success("✅ Emergency alert canceled.")
            st.stop()
            

    # Clear countdown display after completion
    countdown_placeholder.empty()
    cancel_button_placeholder.empty()
    st.session_state.alert_triggered = False

    # Get user location
    location = geocoder.ip("me").latlng if geocoder.ip("me").latlng else "Location Unavailable"

    # Send Emergency Notification via Firebase Cloud Messaging (FCM)
    message = messaging.Message(
        notification=messaging.Notification(
            title="🚨 EMERGENCY ALERT!",
            body=f"User {user_phone} is in danger! 📍 Location: {location}"
        ),
        data={"sound": "beep.mp3"},  # Custom beep sound
        topic="emergency_group"  # Send to all emergency contacts
    )
    response = messaging.send(message)

    # Display success message after countdown
    st.success("🚀 Emergency alert sent successfully!")
    st.write("📍 Location:", location)
    st.write("🔔 Alert sent to:", ", ".join([contact["Contact"] for contact in st.session_state.emergency_contacts]))
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("./main.py")