import streamlit as st
import time
from datetime import datetime
from playsound import playsound

# Title of the app
st.title("💊 Medication Reminder System")

# Initialize reminders list in session state
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# Function to add a new reminder
def add_reminder():
    st.session_state.reminders.append({
        "tablet": "",  # Placeholder for tablet/disease name
        "time": datetime.now().time(),  # Default time
        "triggered": False  # Track if the reminder has been triggered
    })

# Function to remove a reminder
def remove_reminder(index):
    st.session_state.reminders.pop(index)

# Button to add a new reminder
if st.button("➕ Add New Reminder"):
    add_reminder()

# Display and edit existing reminders
for i, reminder in enumerate(st.session_state.reminders):
    st.write(f"### Reminder {i + 1}")

    # Tablet name input
    reminder["tablet"] = st.text_input(f"Enter Tablet Name/Disease for Reminder {i + 1}", 
                                       value=reminder["tablet"], key=f"tablet_{i}")

    # Let the user edit the reminder time
    reminder_time = st.text_input(f"Enter reminder time (HH:MM) for Reminder {i + 1}", 
                                  value=reminder["time"].strftime("%H:%M"), key=f"time_{i}")

    # Update the reminder time in the list
    try:
        reminder["time"] = datetime.strptime(reminder_time, "%H:%M").time()
    except ValueError:
        st.error("Invalid time format. Please enter the time in HH:MM format (e.g., 09:00).")

    # Button to remove the reminder
    if st.button(f"❌ Remove Reminder {i + 1}", key=f"remove_{i}"):
        remove_reminder(i)

# Function to check and alert for all reminders
def check_reminders():
    while True:
        for reminder in st.session_state.reminders:
            current_time = datetime.now().time()
            if not reminder["triggered"] and current_time >= reminder["time"]:
                st.warning(f"🛑 Time to take **{reminder['tablet']}** at {reminder['time']}!")
                st.balloons()  # Fun visual
                try:
                    playsound("./alert_sound.wav")  # Replace with your actual sound file path
                except Exception as e:
                    st.error(f"Error playing sound: {e}")
                reminder["triggered"] = True  # Mark the reminder as triggered
        time.sleep(10)  # Check every 10 seconds

# Button to start all reminders
if st.button("▶️ Start All Reminders"):
    st.write("✅ Medication reminders started...")
    check_reminders()
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("./main.py")
