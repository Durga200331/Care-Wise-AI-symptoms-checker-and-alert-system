import streamlit as st
import json
import os
import subprocess
import time
# Set page config
st.set_page_config(page_title="CureCrafters", layout="wide")



# Apply custom styles
st.markdown(
    """
    <style>
        .title { font-size: 50px; font-weight: bold; text-align: center; color: black; font-family: 'Poppins', sans-serif; }
        .line { width: 100%; height: 2px; background-color: #00AEEF; margin: 20px 0 10px 0; }
        .emergency-button > button { background-color: #FF0000; color: white; padding: 25px; font-size: 50px; border-radius: 12px; width: 60%; margin: auto; display: block; border: none; transition: 0.3s; cursor: pointer; }
        .emergency-button > button:hover { background-color: #CC0000; transform: scale(1.05); }
        .add-contacts-button > button { width: 180px; height: 50px; font-size: 18px; font-weight: bold; border-radius: 8px; background-color: #28a745; color: white; transition: 0.3s; }
        .add-contacts-button > button:hover { background-color: #218838; }
                /* Add Contacts Button (Small & Green) */
        .add-contacts-button > button {
            width: 180px !important;
            height: 50px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            background-color: #28a745 !important;
            color: white !important;
            transition: 0.3s ease-in-out;
        }

        .add-contacts-button > button:hover {
            background-color: #218838 !important;
        }

        /* Other Buttons (Blue) */
        .stButton>button {
            width: 280px !important;
            height: 75px !important;
            font-size: 22px !important;
            font-weight: bold !important;
            border-radius: 14px !important;
            border: none !important;
            background-color: #007BFF !important;
            color: white !important;
            transition: 0.3s ease-in-out;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: auto;
        }

        .stButton>button:hover {
            background-color: #0056b3 !important;
            transform: scale(1.05);
        }

        /* Centered button container */
        .button-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
            margin-top: 50px;
        }

        /* Center the select option text */
        .centered-text {
            text-align: center !important;
            font-size: 28px;
            font-weight: bold;
        }
        

    </style>
     <script>
        document.addEventListener("DOMContentLoaded", function() {
            if (Notification.permission !== "granted") {
                Notification.requestPermission().then(permission => {
                    if (permission === "granted") {
                        console.log("Notification permission granted.");
                    } else {
                        console.warn("Notification permission denied.");
                    }
                });
            }
        });
    </script>
    """,
    unsafe_allow_html=True
)


# Display Title
st.markdown('<h1 style="text-align:center; font-size:50px;">🩺ResQ Your Health!</h1>', unsafe_allow_html=True)

# Line above alert
st.markdown('<div class="line"></div>', unsafe_allow_html=True)
CONTACTS_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file)
    
    # Ensure session state updates properly
    st.session_state.contacts = contacts  


# Initialize session state for contacts and form visibility
if "contacts" not in st.session_state:
    st.session_state.contacts = load_contacts()
    st.session_state.emergency_contacts = st.session_state.contacts
if "show_contact_form" not in st.session_state:
    st.session_state.show_contact_form = False


# Emergency Button
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
    if st.button("🚨 Emergency", key="emergency_button"):
        st.session_state.alert_triggered = True
        st.session_state.start_time = time.time()
        st.success("⚡ Emergency alert triggered! Redirecting to emergency page...")

        # Redirect to emergency.py
        st.switch_page("pages/emergency.py")
    st.markdown("</div>", unsafe_allow_html=True)


# Small "Add Contacts" Button
st.markdown('<div class="add-contacts-button" style="text-align:center; margin-top: 10px;">', unsafe_allow_html=True)

# # Toggle the contact form when "Add Contacts" is clicked
# if :
#     st.session_state.show_contact_form = True

# my_phone_number = [
#     '+919182747876',
#     '+919014070363',
#     '+919030102683'
# ]

# # User Input for Additional Phone Number
# new_number = st.text_input("Enter a phone number (with country code) to add:", "")

# # Append the new number if it's valid
# if new_number.startswith("+") and len(new_number) > 10:
#     if new_number not in my_phone_number:
#         my_phone_number.append(new_number)
#         st.success(f"✅ {new_number} added to the contact list!")
#     else:
#         st.warning("⚠️ This number is already in the list.")
# elif new_number:
#     st.error("❌ Please enter a valid phone number with country code (e.g., +919876543210)")
# Display the contact form only if toggled
# if st.session_state.show_contact_form:
#     with st.form("contact_form"):
#         user_number = st.text_input("Enter Your Number (📱) (Optional)")
#         new_contacts = st.text_area("Enter Emergency Contact Numbers (📞) (One per line)")
#         submit_button = st.form_submit_button("Save Contacts")

#         if submit_button:
#             contact_list = [num.strip() for num in new_contacts.split("\n") if num.strip()]
#             if contact_list:
#                 contacts = [{"User": user_number if user_number else "Not Provided", "Contact": contact} for contact in contact_list]
#                 save_contacts(contacts)
#                 st.session_state.contacts = contacts
#                 st.success(f"✅ {len(contact_list)} Contact(s) Saved Successfully!")
#                 st.write("✅contacts saved succesfully ")
#                 st.session_state.show_contact_form = False
#                 st.rerun()
# Centered Page Header
st.markdown('<div class="centered-text">Select an Option</div>', unsafe_allow_html=True)

# Centered Buttons
st.markdown('<div class="button-container">', unsafe_allow_html=True)

# Creating evenly spaced buttons in a flexible layout
col1, col2 = st.columns(2)

with col1:
    if st.button("📸 Capture Symptoms"):
        st.switch_page("pages/capture.py")

    st.write("")  # Spacer

    if st.button("📍 Nearest Clinics"):
        st.switch_page("pages/nearbyclinics.py")

with col2:
    if st.button("🔍 Check Symptoms"):
        st.switch_page("pages/Symptom_Check.py")

    st.write("")  # Spacer

    if st.button("⏰ Medicine Alarm"):
        st.switch_page("pages/remainder.py")

st.markdown('</div>', unsafe_allow_html=True)