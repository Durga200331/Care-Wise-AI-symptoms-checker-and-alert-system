import streamlit as st
import geocoder
import requests

def get_nearby_hospitals_osm(lat, lon):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": "hospital",
        "format": "json",
        "limit": 6,
        "lat": lat,
        "lon": lon,
        "bounded": 1,
        "viewbox": f"{lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}"
    }
    headers = {
        "User-Agent": "HospitalLocator/1.0 (your_email@example.com)"  # Replace with your email
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        hospitals = response.json()

        if not hospitals:
            return "No hospitals found nearby."

        return hospitals

    except requests.exceptions.RequestException as e:
        return f"API Request Failed: {e}"
    except requests.exceptions.JSONDecodeError:
        return "Invalid JSON response from API."

# Streamlit UI
st.title("Nearby Hospitals/Clinics")

g = geocoder.ip('me')
if g.latlng:
    lat, lon = g.latlng
    st.write(f"Your Location: Latitude {lat}, Longitude {lon}")

    hospitals = get_nearby_hospitals_osm(lat, lon)

    if isinstance(hospitals, str):
        st.error(hospitals)
    else:
        cols = st.columns(2)
        for i, hospital in enumerate(hospitals):
            display_name = hospital.get('display_name', '')
            address_data = hospital.get('address', {})
            full_address = display_name #if no address data exists, display the display name.
            if address_data:
                full_address = ", ".join(filter(None, [address_data.get('house_number'), address_data.get('road'), address_data.get('neighbourhood'), address_data.get('city'), address_data.get('town'), address_data.get('village')]))

            website = hospital.get('website')
            with cols[i % 2]:
                st.subheader(hospital.get('display_name', 'Unknown Hospital'))
                # st.write(f"Address: {full_address}")
                st.markdown("---")

else:
    st.error("Could not fetch your location. Try again.")
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("./main.py")