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

PRO_PASSWORD = "UNLIMITED2026"

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .header-box {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/sparkles.png", width=60)
    st.title("PixelForge Pro")
    
    if st.session_state.is_pro:
        st.success("🌟 **Pro Active** (Unlimited & No Ads)")
    else:
        st.info(f"⚡ Free Credits: **{st.session_state.generations_left} remaining**")
        st.write("---")
        st.subheader("🔑 Unlock Pro Access")
        passcode_input = st.text_input("Enter Passcode:", type="password")
        if st.button("Activate Passcode"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro status unlocked!")
                st.rerun()
            else:
                st.error("Invalid key.")

# --- FULL-SCREEN AD OVERLAY MODAL ---
@st.dialog(" ", width="large")
def show_ad_modal():
    # Force full-screen blackout styling
    st.markdown("""
        <style>
        div[data-testid="stDialog"] > div {
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
            background-color: #000000 !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 999999 !important;
        }
        button[aria-label="Close"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #ff4b4b; margin-bottom: 5px;'>📺 SPONSORED AD BREAK</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Your high-resolution AI image is generating in the background...</p>", unsafe_allow_html=True)
    
    # YOUR ADSTERRA SCRIPT EMBED
    ad_code = """
    <div style="text-align:center; padding: 20px;">
        <script src="https://pl30779296.effectivecpmnetwork.com/1e/38/20/1e3820839b36df037dab169eee1f0358.js"></script>
    </div>
    """
    components.html(ad_code, height=300)
    
    # 10-Second Unskippable Countdown Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    wait_time = 10
    for i in range(wait_time):
        time.sleep(1)
        progress = int(((i + 1) / wait_time) * 100)
        progress_bar.progress(progress)
        status_text.markdown(f"<h3 style='text-align: center; color: #38bdf8; margin-top: 10px;'>⏳ Unlocking in {wait_time - (i + 1)}s...</h3>", unsafe_allow_html=True)
    
    status_text.empty()
    progress_bar.empty()
    st.rerun()

# --- MAIN APP UI ---
st.markdown("""
<div class="header-box">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨 PixelForge AI</h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">Transform text prompts into stunning artwork in seconds</p>
</div>
""", unsafe_allow_html=True)

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
            with st.spinner("Rendering your artwork..."):
                full_prompt = prompt if style == "None" else f"{prompt}, {style} style"
                encoded_prompt = urllib.parse.quote(full_prompt)
                
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
                        st.session_state.generated_image_bytes = response.content
                        st.session_state.current_caption = f"“{full_prompt}”"
                        
                        if not st.session_state.is_pro:
                            st.session_state.generations_left -= 1
                            show_ad_modal()
                        else:
                            st.rerun()
                    else:
                        st.error("Server busy, try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type a description first!")

else:
    st.markdown("""
    <div class="card-box" style="border: 2px solid #ef4444; text-align: center;">
        <h2 style="color: #ef4444;">🔒 Free Credits Exhausted</h2>
        <p style="color: #cbd5e1;">You've used all 3 free image generations.</p>
        <p>Subscribe to Pro for <b>instant generations</b>, <b>zero ad breaks</b>, and <b>unlimited high-res downloads</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("[👉 **Click Here to Subscribe for $5/month on Gumroad**](https://daniel.gumroad.com)")

# --- DISPLAY RESULT ---
if st.session_state.generated_image_bytes:
    st.write("---")
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

PRO_PASSWORD = "UNLIMITED2026"

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .header-box {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/sparkles.png", width=60)
    st.title("PixelForge Pro")
    
    if st.session_state.is_pro:
        st.success("🌟 **Pro Active** (Unlimited & No Ads)")
    else:
        st.info(f"⚡ Free Credits: **{st.session_state.generations_left} remaining**")
        st.write("---")
        st.subheader("🔑 Unlock Pro Access")
        passcode_input = st.text_input("Enter Passcode:", type="password")
        if st.button("Activate Passcode"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro status unlocked!")
                st.rerun()
            else:
                st.error("Invalid key.")

# --- FULL-SCREEN AD OVERLAY MODAL ---
@st.dialog(" ", width="large")
def show_ad_modal():
    st.markdown("""
        <style>
        div[data-testid="stDialog"] > div {
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
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

PRO_PASSWORD = "UNLIMITED2026"

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .header-box {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/sparkles.png", width=60)
    st.title("PixelForge Pro")
    
    if st.session_state.is_pro:
        st.success("🌟 **Pro Active** (Unlimited & No Ads)")
    else:
        st.info(f"⚡ Free Credits: **{st.session_state.generations_left} remaining**")
        st.write("---")
        st.subheader("🔑 Unlock Pro Access")
        passcode_input = st.text_input("Enter Passcode:", type="password", key="sidebar_passcode_input")
        if st.button("Activate Passcode", key="sidebar_passcode_btn"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro status unlocked!")
                st.rerun()
            else:
                st.error("Invalid key.")

# --- FULL-SCREEN AD OVERLAY MODAL ---
@st.dialog(" ", width="large")
def show_ad_modal():
    st.markdown("""
        <style>
        div[data-testid="stDialog"] > div {
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
            background-color: #000000 !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 999999 !important;
        }
        button[aria-label="Close"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #ff4b4b; margin-bottom: 5px;'>📺 SPONSORED AD BREAK</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Your high-resolution AI image is generating in the background...</p>", unsafe_allow_html=True)
    
    ad_code = """
    <div style="text-align:center; padding: 20px;">
        <script src="https://pl30779296.effectivecpmnetwork.com/1e/38/20/1e3820839b36df037dab169eee1f0358.js"></script>
    </div>
    """
    components.html(ad_code, height=300)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    wait_time = 10
    for i in range(wait_time):
        time.sleep(1)
        progress = int(((i + 1) / wait_time) * 100)
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

PRO_PASSWORD = "UNLIMITED2026"

# --- CUSTOM CSS STYLING ---
# Ensure the triple quotes (""") stay intact so Python knows this is CSS!
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .header-box {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "generated_image_bytes" not in st.session_state:
    st.session_state.generated_image_bytes = None
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/sparkles.png", width=60)
    st.title("PixelForge Pro")
    
    if st.session_state.is_pro:
        st.success("🌟 **Pro Active** (Unlimited & No Ads)")
    else:
        st.info(f"⚡ Free Credits: **{st.session_state.generations_left} remaining**")
        st.write("---")
        st.subheader("🔑 Unlock Pro Access")
        passcode_input = st.text_input("Enter Passcode:", type="password", key="sidebar_passcode_input")
        if st.button("Activate Passcode", key="sidebar_passcode_btn"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro status unlocked!")
                st.rerun()
            else:
                st.error("Invalid key.")

# --- FULL-SCREEN AD OVERLAY MODAL ---
@st.dialog(" ", width="large")
def show_ad_modal():
    st.markdown("""
        <style>
        div[data-testid="stDialog"] > div {
            width: 100vw !important;
            height: 100vh !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
            background-color: #000000 !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 999999 !important;
        }
        button[aria-label="Close"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #ff4b4b; margin-bottom: 5px;'>📺 SPONSORED AD BREAK</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Your high-resolution AI image is generating in the background...</p>", unsafe_allow_html=True)
    
    ad_code = """
    <div style="text-align:center; padding: 20px;">
        <script src="https://pl30779296.effectivecpmnetwork.com/1e/38/20/1e3820839b36df037dab169eee1f0358.js"></script>
    </div>
    """
    components.html(ad_code, height=300)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    wait_time = 10
    for i in range(wait_time):
        time.sleep(1)
        progress = int(((i + 1) / wait_time) * 100)
        progress_bar.progress(progress)
        status_text.markdown(f"<h3 style='text-align: center; color: #38bdf8; margin-top: 10px;'>⏳ Unlocking in {wait_time - (i + 1)}s...</h3>", unsafe_allow_html=True)
    
    status_text.empty()
    progress_bar.empty()
    st.rerun()

# --- MAIN APP UI ---
st.markdown("""
<div class="header-box">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨 PixelForge AI</h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">Transform text prompts into stunning artwork in seconds</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card-box">', unsafe_allow_html=True)
prompt = st.text_input("Prompt:", placeholder="e.g., A cybernetic samurai in cyberpunk Tokyo, 8k resolution", key="main_prompt_input")
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Art Style:", ["None", "Cyberpunk", "Anime", "Photorealistic", "Digital Painting", "3D Render", "Fantasy"], key="main_style_select")
with col2:
    aspect_ratio = st.selectbox("Aspect Ratio:", ["Square (1:1)", "Portrait (3:4)", "Landscape (16:9)"], key="main_aspect_select")
st.markdown('</div>', unsafe_allow_html=True)

can_generate = st.session_state.is_pro or st.session_state.generations_left > 0

# --- GENERATION LOGIC ---
if can_generate:
    if st.button("✨ Generate Artwork", type="primary", key="generate_art_btn"):
        if prompt.strip():
            with st.spinner("Rendering your artwork..."):
                full_prompt = prompt if style == "None" else f"{prompt}, {style} style"
                encoded_prompt = urllib.parse.quote(full_prompt)
                
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
                        st.session_state.generated_image_bytes = response.content
                        st.session_state.current_caption = f"“{full_prompt}”"
                        
                        if not st.session_state.is_pro:
                            st.session_state.generations_left -= 1
                            show_ad_modal()
                        else:
                            st.rerun()
                    else:
                        st.error("Server busy, try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type a description first!")

else:
    st.markdown("""
    <div class="card-box" style="border: 2px solid #ef4444; text-align: center;">
        <h2 style="color: #ef4444;">🔒 Free Credits Exhausted</h2>
        <p style="color: #cbd5e1;">You've used all 3 free image generations.</p>
        <p>Subscribe to Pro for <b>instant generations</b>, <b>zero ad breaks</b>, and <b>unlimited high-res downloads</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("[👉 **Click Here to Subscribe for $5/month on Gumroad**](https://daniel.gumroad.com)")

# --- DISPLAY RESULT ---
if st.session_state.generated_image_bytes:
    st.write("---")
    st.markdown("### 🖼️ Your Generated Artwork")
    st.image(st.session_state.generated_image_bytes, caption=st.session_state.current_caption, use_container_width=True)
    st.download_button(
        label="📥 Download High-Res Image",
        data=st.session_state.generated_image_bytes,
        file_name="pixelforge_artwork.png",
        mime="image/png",
        key="download_img_btn"
    )
