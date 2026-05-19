# Change this:
# from Nordale import NordaleEngine, ai_translate

# To this:
import sys
# Add current directory to path so it can find Nordale.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Nordale import NordaleEngine, ai_translate

# Initialize the translation engine
translator = NordaleEngine()
NORDALIAN_DICTIONARY = translator.NORDALIAN_DICTIONARY

def local_translate(text: str) -> str:
    return translator.local_translate(text)

# ==============================================================================
# STREAMLIT USER INTERFACE
# ==============================================================================
st.set_page_config(page_title="Nordalian Language Translator", page_icon="🚂", layout="centered")

# Sidebar - Settings and Documentation
with st.sidebar:
    st.subheader("🔑 Engine Settings")
    
    default_key = os.environ.get("GEMINI_API_KEY", "")
    user_key = st.text_input("Enter Gemini API Key:", value=default_key, type="password")
    
    if user_key:
        st.success("🟢 Custom AI Engine Active")
    else:
        st.info("🟡 Running on Local Dictionary Fallback")

    with st.expander("ℹ️ How to get a free API Key"):
        st.markdown("""
        To unlock advanced AI grammar features without using the shared fallback pool, you can get a free key from Google in less than a minute:
        
        1. Go to **[Google AI Studio](https://aistudio.google.com/)** and sign in with any standard Google account.
        2. Click the prominent **"Create API Key"** button at the top left.
        3. Select **"Create API key in new project"**.
        4. Copy the long string of letters and numbers generated for you.
        5. Paste it right into the box above and hit **Enter**!
        """)
        
    st.markdown("---")
    st.markdown("### 💰 Token Usage & Cost Transparency")
    st.info("""
    **Why is an API Key needed?**
    Advanced AI translation runs on Google's infrastructure, which charges based on the length of text processed (tokens). 
    
    Using a personal free key or letting the app roll over to the built-in *Local Fallback Loop* is always 100% free!
    """)

    st.markdown("---")
    st.markdown("""
    ### 🗺️ Federation Demographics
    🔧 Faction Sectors:
    * **English**: Capitals & Ports Layout Framework
    * **Germans**: Mainline Heavy Steel & Machining
    * **Dutch**: Canal Switch & Hydrological Networks
    * **Norwegians**: Mountain Pass Infrastructure
    * **Welsh-Adjacent**: Narrow-Gauge Valley Coal Mining
    * **Romance Native**: Agrarian Valleys, Weather, & Time
    """)

# Main Content Interface
st.title("🚂 Nordalian Language Translator")
st.markdown("Convert standard English into Nordalian rail pidgin seamlessly.")

english_text = st.text_area("Enter English Text:", placeholder="The heavy steel wagon is stuck on the steep incline.")

if st.button("Translate", type="primary"):
    if not english_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Processing regional dialects..."):
            if user_key:
                try:
                    from google import genai
                    client = genai.Client(api_key=user_key)
                    
                    # Capture translation and word dict
                    result, new_words = ai_translate(english_text, client, translator)
                    
                    # Direct, unfiltered feed into dictionary.json
                    if new_words:
                        translator.save_new_words(new_words)
                    
                    st.subheader("Nordalian Pidgin:")
                    st.code(result, language=None)
                    st.caption("Processed via: Gemini AI Engine (Substrate Dynamic Integration + Silent Learning Active)")
                except Exception as e:
                    result = local_translate(english_text)
                    st.subheader("Nordalian Pidgin:")
                    st.code(result, language=None)
                    st.error(f"Processed via: Local Fallback Loop (AI Error: {e})")
            else:
                result = local_translate(english_text)
                st.subheader("Nordalian Pidgin:")
                st.code(result, language=None)
                st.caption("Processed via: Local Dictionary Fallback Loop")