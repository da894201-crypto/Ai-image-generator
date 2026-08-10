import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PixelForge AI - Instant Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)

PRO_PASSWORD = "UNLIMITED2026"  # Set your Pro Key here

# --- CUSTOM MODERN CSS STYLING ---
st.markdown("""
<style>
    /* Dark Gradient Theme & Clean Typography */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Header Container */
    .header-box {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Card Container */
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    
    /* Styled Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""

# --- SIDEBAR ACCESS SYSTEM ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/sparkles.png", width=60)
    st.title("PixelForge Pro")
    
    if st.session_state.is_pro:
        st.success("🌟 **Pro Active** (Unlimited & No Ads)")
    else:
        st.info(f"⚡ Free Credits: **{st.session_state.generations_left} remaining**")
        st.write("---")
        st.subheader("🔑 Unlock Pro Access")
        passcode_input = st.text_input("Enter Passcode:", type="password", help="Found on your Gumroad receipt")
        if st.button("Activate Passcode"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro status unlocked!")
                st.rerun()
            else:
                st.error("Invalid key. Please try again.")

# --- FULL-SCREEN AD MODAL DIALOG ---
@st.dialog("📺 Sponsored Ad Break", width="large")
def show_ad_modal():
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Please watch this brief sponsor ad while your high-resolution AI image is prepared.</p>", unsafe_allow_html=True)
    
    # --- PASTE YOUR REAL ADSTERRA / AD CODE BELOW ---
    ad_code = """
    <div style="text-align:center; padding: 15px; background: #000; border-radius: 12px; border: 1px solid #334155;">
        <!-- Replace this iframe with your Adsterra snippet code -->
        <script>
            atOptions = {
              'key' : '44e2d4b48a05c0ee3122df925d28026e',
              'format' : 'iframe',
              'height' : 250,
              'width' : 300,
              'params' : {}
           };
       </script>
       <script src="https://www.highperformanceformat.com/44e2d4b48a05c0ee3122df925d28026e/invoke.js"></script>

    </div>
    """
    components.html(ad_code, height=280)
    
    # Countdown Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    wait_time = 10
    for i in range(wait_time):
        time.sleep(1)
        progress = int(((i + 1) / wait_time) * 100)
        progress_bar.progress(progress)
        status_text.markdown(f"<h4 style='text-align: center; color: #38bdf8;'>⏳ Unlocking image in {wait_time - (i + 1)}s...</h4>", unsafe_allow_html=True)
    
    st.success("🎉 Image ready!")
    time.sleep(0.5)
    st.rerun()

# --- MAIN APP INTERFACE ---
st.markdown("""
<div class="header-box">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨 PixelForge AI</h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">Transform text prompts into stunning artwork in seconds</p>
</div>
""", unsafe_allow_html=True)

# Prompt Inputs Inside Card
st.markdown('<div class="card-box">', unsafe_allow_html=True)
prompt = st.text_input("Prompt:", placeholder="e.g., A cybernetic samurai in cyberpunk Tokyo, 8k resolution")
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Art Style:", ["None", "Cyberpunk", "Anime", "Photorealistic", "Digital Painting", "3D Render", "Fantasy"])
with col2:
    aspect_ratio = st.selectbox("Aspect Ratio:", ["Square (1:1)", "Portrait (3:4)", "Landscape (16:9)"])
st.markdown('</div>', unsafe_allow_html=True)

can_generate = st.session_state.is_pro or st.session_state.generations_left > 0

# --- GENERATION LOGIC ---
if can_generate:
    if st.button("✨ Generate Artwork", type="primary"):
        if prompt.strip():
            with st.spinner("Rendering your image from AI servers..."):
                full_prompt = prompt if style == "None" else f"{prompt}, {style} style"
                encoded_prompt = urllib.parse.quote(full_prompt)
                
                # Dimensions setup
                width, height = 1024, 1024
                if aspect_ratio == "Portrait (3:4)":
                    width, height = 768, 1024
                elif aspect_ratio == "Landscape (16:9)":
                    width, height = 1024, 576
                
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
                
                try:
                    response = requests.get(image_url, headers=headers, timeout=30)
                    if response.status_code == 200:
                        # Save image data to state so it doesn't disappear
                        st.session_state.generated_image_bytes = response.content
                        st.session_state.current_caption = f"“{full_prompt}”"
                        
                        # Deduct credit if free
                        if not st.session_state.is_pro:
                            st.session_state.generations_left -= 1
                            # Trigger Full-Screen Ad Dialog
                            show_ad_modal()
                        else:
                            st.rerun()
                    else:
                        st.error("AI Server is busy. Please try clicking generate again!")
                except Exception as e:
                    st.error(f"Network error: {e}")
        else:
            st.warning("Please type a description in the prompt box first!")

else:
    # --- PAYWALL CARD ---
    st.markdown("""
    <div class="card-box" style="border: 2px solid #ef4444; text-align: center;">
        <h2 style="color: #ef4444;">🔒 Free Credits Exhausted</h2>
        <p style="color: #cbd5e1;">You've used all 3 free image generations for this session.</p>
        <p>Subscribe to Pro for <b>instant generations</b>, <b>zero ad breaks</b>, and <b>unlimited high-res downloads</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("[👉 **Click Here to Subscribe for $5/month on Gumroad**](https://daniel.gumroad.com)")

# --- DISPLAY GENERATED IMAGE ---
if st.session_state.generated_image_bytes:
    st.write("---")
    st.markdown("### 🖼️ Your Generated Artwork")
    st.image(st.session_state.generated_image_bytes, caption=st.session_state.current_caption, use_container_width=True)
    
    # Download Button
    st.download_button(
        label="📥 Download High-Res Image",
        data=st.session_state.generated_image_bytes,
        file_name="pixelforge_artwork.png",
        mime="image/png"
    )
