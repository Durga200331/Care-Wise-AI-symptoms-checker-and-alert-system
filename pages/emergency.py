import streamlit as st
from twilio.rest import Client
import geocoder  # For live location

# Streamlit Page Configuration
st.set_page_config(page_title="Send Location SMS Using Twilio", page_icon="📩")

# Page Header
st.title("📩 Send Live Location SMS")
st.write("Enter a phone number to add it to the emergency contact list and send your live location.")

# Twilio Credentials
account_sid = "ACb876612cde4f639bed4260001a664362"
auth_token = "14259187cb019f6264119e2db2eb3ca7"
twilio_number = "+19064989917"

# Default List of Emergency Contacts
my_phone_number1 = [
   
    '+919014070363',
    '+919030102683'
]

# User Input for Additional Phone Number
new_number = st.text_input("Enter a phone number (with country code) to add:", "")

# Append the new number if it's valid
if new_number.startswith("+") and len(new_number) > 10:
    if new_number not in my_phone_number1:
        my_phone_number1.append(new_number)
        st.success(f"✅ {new_number} added to the contact list!")
    else:
        st.warning("⚠️ This number is already in the list.")
elif new_number:
    st.error("❌ Please enter a valid phone number with country code (e.g., +919876543210)")

# Function to get live location
def get_location():
    g = geocoder.ip('me')
    if g.latlng:
        latitude, longitude = g.latlng
        google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        return latitude, longitude, google_maps_link
    else:
        return None, None, None

# Button to Send SMS
if st.button("📩 Send Emergency Alert"):
    # Get the live location
    latitude, longitude, google_maps_link = get_location()

    if latitude and longitude:
        # Twilio Client
        client = Client(account_sid, auth_token)

        # Send SMS with location
        message_body = f"""
        🚨 Emergency Alert!
        The person has shared their live location.

        📍 Location: {google_maps_link}
        """
        for number in my_phone_number1:
            message = client.messages.create(
                from_=twilio_number,
                body=message_body,
                to=number
            )

        # Make an Emergency Call
        for number in my_phone_number1:
            call = client.calls.create(
                twiml='<Response><Say>This is an emergency alert. Please check your SMS for the location details.</Say></Response>',
                to=number,
                from_=twilio_number
            )

        # Show Success Message
        st.success(f"✅ SMS Sent Successfully to {my_phone_number1}!")
        st.write("Live Location:", google_maps_link)
        st.write("Message SID:", message.sid)
    else:
        st.error("❌ Failed to fetch live location. Please try again.")

        
        
# # Countdown Timer Before Sending Alert
# if "alert_triggered" in st.session_state and st.session_state.alert_triggered:
#     countdown = 3  # Set countdown to 5 seconds
#     countdown_placeholder = st.empty()
#     cancel_button_placeholder = st.empty()

#     for i in range(countdown, 0, -1):
#         countdown_placeholder.markdown(f"<h1 style='text-align: center; color: red;'>{i}</h1>", unsafe_allow_html=True)
#         time.sleep(1)

#         # Allow canceling the alert at any time
#         if cancel_button_placeholder.button("❌ Cancel Alert", key=f"cancel_{i}"):
#             st.session_state.alert_triggered = False
#             countdown_placeholder.empty()
#             cancel_button_placeholder.empty()
#             st.success("✅ Emergency alert canceled.")
#             st.stop()
            

#     # Clear countdown display after completion
#     countdown_placeholder.empty()
#     cancel_button_placeholder.empty()
#     st.session_state.alert_triggered = False        