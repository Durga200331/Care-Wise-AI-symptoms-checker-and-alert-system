import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import re

genai.configure(api_key="AIzaSyDLVQkoApzbzXzRdn_9gAQ-L0AcQJCbM2A")

st.title("Medical Image Analysis with Gemini AI")

option = st.radio("Choose Image Input Method:", ("Upload Image", "Capture from Camera"))

image = None
if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image for analysis", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        image_bytes = uploaded_file.getvalue()

elif option == "Capture from Camera":
    captured_image = st.camera_input("Take a picture for analysis")
    if captured_image:
        image = Image.open(captured_image)
        st.image(image, caption="Captured Image", use_container_width=True)
        image_bytes = captured_image.getvalue()

if image:
    symptoms = st.text_area("Describe your symptoms (optional):")
    analyze_button = st.button("Analyze Image")

    if analyze_button:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            "**Analyze this medical image and provide a structured response in Markdown format:**\n\n"
            "### Severity Level\n"
            "Provide a severity level as 'Severity Level: X%' without additional text.\n\n"
            "### Causes\n"
            "List the possible causes in simple terms (avoid complex medical jargon).\n\n"
            "### Remedies\n"
            "Suggest effective **home remedies** using Ayurveda, Traditional Chinese Medicine (TCM), and Unani practices.\n\n"
            "### Diet Suggestions\n"
            "List foods to **eat** and **avoid** for faster recovery.\n\n"
            "### Consequences\n"
            "Explain what happens if left untreated (in simple terms).\n\n"
            "### Emergency Actions\n"
            "When is urgent medical attention required?"
        )

        input_data = [prompt, image]
        if symptoms:
            input_data.append(f"**User Symptoms:** {symptoms}")

        response = model.generate_content(input_data)
        response_text = response.text.strip()

        # Extract Severity Level from AI response
        severity_level = 50  # Default placeholder
        match = re.search(r"Severity Level:\s*(\d+)%", response_text)
        if match:
            severity_level = int(match.group(1))

        st.subheader("AI Analysis Results:")
        st.progress(severity_level / 100)
        st.write(f"**Severity Level:** {severity_level}%")

        # Define structured sections
        sections = ["Causes", "Remedies", "Diet Suggestions", "Consequences", "Emergency Actions"]

        # Extract section data properly
        response_data = {}
        for section in sections:
            pattern = rf"### {section}\n(.*?)(?=\n###|\Z)"
            match = re.search(pattern, response_text, re.DOTALL)
            response_data[section] = match.group(1).strip() if match else "No information available."

        # Responsive layout using columns
        cols = st.columns(2)  # Create two columns

        for i, title in enumerate(sections):
            col = cols[i % 2]  # Alternate between columns
            with col:
                with st.container():
                    st.markdown(f"### {title}")
                    st.info(response_data[title])

        # Emergency Warning
        if severity_level > 80:
            st.error("⚠️ This condition may require urgent medical attention!")
            if st.button("Find a Doctor Near Me"):
                st.write("Redirecting to doctor search...")
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.switch_page("./main.py")