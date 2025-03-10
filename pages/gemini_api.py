import google.generativeai as genai

# Set Gemini API Key
API_KEY = "AIzaSyBwLamVqNqwrB8TL4lmt3hb8i8tJSwHDrg"
genai.configure(api_key=API_KEY)

def analyze_symptoms(body_part, symptoms):
    """Call Gemini AI API to analyze symptoms and provide structured recommendations."""
    
    prompt = f"""
    You are a medical AI assistant. Please analyze the following symptoms and provide a structured health response.

    ### **Patient Details**
    - **Body Part Affected:** {body_part}
    - **Reported Symptoms:** {', '.join(symptoms)}

    ### **Instructions for Response**
    Provide a structured and **medically relevant** response that includes:

    **Diagnosis:**  
    - [Provide the diagnosis and a short explanation]

    **Food to Eat:**  
    - ✅ [Food Item 1] – [Why it’s beneficial]  
    - ✅ [Food Item 2] – [Why it’s beneficial]  
    - ✅ [Food Item 3] – [Why it’s beneficial]  

    **Food to Avoid:**  
    - ❌ [Food Item 1] – [Why it’s harmful]  
    - ❌ [Food Item 2] – [Why it’s harmful]  
    - ❌ [Food Item 3] – [Why it’s harmful]  

    **Activities to Do:**  
    - ✅ [Activity 1] – [How it helps]  
    - ✅ [Activity 2] – [How it helps]  
    - ✅ [Activity 3] – [How it helps]  

    **Activities to Avoid:**  
    - ❌ [Activity 1] – [Why it’s harmful]  
    - ❌ [Activity 2] – [Why it’s harmful]  
    - ❌ [Activity 3] – [Why it’s harmful]  

    Ensure that your response is **medically sound**, easy to read, and formatted exactly as requested.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text  # Return structured response as text
