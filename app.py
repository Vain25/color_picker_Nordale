import streamlit as st
import os
from Nordale import local_translate, ai_translate

# 1. Set up the browser tab title and layout
st.set_page_config(page_title="Nordalian Translator", page_icon="🚂", layout="centered")

# 2. Design the visual Header
st.title("🚂 Nordalian Language Translator")
st.write("Convert standard English into Nordalian rail pidgin seamlessly.")

# --- API KEY MANAGEMENT SIDEBAR ---
st.sidebar.header("🔑 Engine Settings")

# Check system environment first
system_key = os.environ.get("GEMINI_API_KEY")
user_key = None

if system_key:
    st.sidebar.success("🟢 Using Developer System Key")
    active_key = system_key
else:
    # If no system key, provide an option for users to input theirs
    st.sidebar.write("To use advanced AI grammar features, provide a Gemini API Key. Otherwise, the app uses the local dictionary fallback.")
    user_key = st.sidebar.text_input("Enter Gemini API Key:", type="password", help="Grab a free key from Google AI Studio")
    
    if user_key:
        st.sidebar.success("🟢 Custom User Key Active")
        active_key = user_key
    else:
        st.sidebar.warning("🟡 Local Dictionary Fallback Active")
        active_key = None

# 3. Initialize the correct engine based on key availability
if active_key:
    try:
        from google import genai
        # Initialize the client with the explicitly selected key
        client = genai.Client(api_key=active_key)
        translate_func = lambda text: ai_translate(text, client)
    except Exception as e:
        st.error(f"Failed to initialize AI Engine: {e}. Defaulting to dictionary fallback.")
        translate_func = local_translate
else:
    translate_func = local_translate

st.divider()

# 4. Create the Text Box UI elements
user_input = st.text_area("Enter English Text:", placeholder="Type your sentence here... (e.g., The green train did not stop at the big station.)")

# 5. Create a click button to trigger the translation
if st.button("Translate to Nordalian", type="primary"):
    if user_input.strip():
        with st.spinner("Processing language structures..."):
            try:
                result = translate_func(user_input)
                # Display the output in a nice visual box
                st.subheader("Nordalian Output:")
                st.info(result)
            except Exception as api_err:
                st.error(f"API Error encountered: {api_err}. Check your key or try again.")
    else:
        st.error("Please enter some text first!")