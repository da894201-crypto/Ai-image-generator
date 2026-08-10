import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PixelForge AI - Instant Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)

PRO_PASSWORD = "UNLIMITED2026"

# 🔴 YOUR ACTIVE ADSTERRA DIRECT LINK 🔴
ADSTERRA_DIRECT_LINK = "https://www.effectivecpmnetwork.com/vqwptfhf7e?key=387fee6ebf196f7838452f5a26520fb4"

# --- CHECK UNLOCK URL PARAMETER ---
query_params = st.query_params
if query_params.get("unlocked") == "true":
    st.session_state.is_locked = False

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 60%, #090d16 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    div[data-testid="stWidgetInstructions"], 
    small[data-testid="stWidgetInstructions"],
    [data-testid="InputInstructions"] {
        display: none !important;
    }
    .header-box {
        text-align: center;
        padding: 2.2rem 1.2rem 1.2rem 1.2rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.8rem;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        padding: 1.6rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 0.75rem 1.2rem !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0f19 0%, #05070d 100%) !important;
    }
    .credit-badge {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""
if "is_locked" not in st.session_state:
    st.session_state.is_locked = False

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("## 🎨 PixelForge Pro")
    if st.session_state.is_pro:
        st.success("🌟 PRO UNLOCKED")
    else:
        st.markdown(f'<div class="credit-badge">⚡ Free Credits: <b>{st.session_state.generations_left}</b></div>', unsafe_allow_html=True)
        passcode_input = st.text_input("Passcode", type="password", placeholder="Enter passcode...")
        if st.button("Activate Passcode"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro activated!")
                st.rerun()

# --- HEADER ---
st.markdown("""
<div class="header-box">
    <div class="header-title">🎨 PixelForge AI</div>
    <p style="color: #94a3b8;">Transform text prompts into stunning artwork</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT CARD ---
st.markdown('<div class="card-box">', unsafe_allow_html=True)
prompt = st.text_input("Prompt:", placeholder="e.g., A futuristic cybernetic knight", key="main_prompt")
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Style:", ["None", "Cyberpunk", "Anime", "Photorealistic", "Fantasy"])
with col2:
    aspect_ratio = st.selectbox("Ratio:", ["Square (1:1)", "Portrait (3:4)", "Landscape (16:9)"])
st.markdown('</div>', unsafe_allow_html=True)

# --- GENERATION ---
can_generate = st.session_state.is_pro or st.session_state.generations_left > 0

if can_generate:
    if st.button("✨ Generate Artwork", type="primary"):
        if prompt.strip():
            with st.spinner("Rendering artwork..."):
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
                        # SAVE IMAGE TO DISK TO PREVENT DATA LOSS ON RELOAD
                        with open("temp_art.png", "wb") as f:
                            f.write(response.content)
                        
                        st.session_state.current_caption = f"“{full_prompt}”"
                        
                        if not st.session_state.is_pro:
                            st.session_state.generations_left -= 1
                            st.session_state.is_locked = True
                        else:
                            st.session_state.is_locked = False
                        st.rerun()
                    else:
                        st.error("Server busy, try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt!")

# --- DISPLAY RESULT ---
if os.path.exists("temp_art.png"):
    st.write("---")
    st.markdown("### 🖼️ Your Generated Artwork")
    
    if st.session_state.is_locked:
        st.markdown("""
        <div class="card-box" style="text-align: center; border: 1px solid #3b82f6;">
            <h3 style="margin-top: 0; color: #60a5fa;">🔓 Image Ready To Unlock</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Tap Step 1 to open the sponsor link and immediately unlock Step 2.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enforced Lock (Step 2 is physically unclickable until Step 1 is clicked)
        components.html(
            f"""
            <div style="font-family: system-ui, -apple-system, sans-serif; text-align: center;">
                <button id="step1-btn" onclick="openAdAndUnlock()" 
                        style="width: 100%; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: #ffffff; font-weight: 800; font-size: 1.1rem; padding: 1rem; border-radius: 12px; border: none; cursor: pointer; box-shadow: 0 8px 20px rgba(34, 197, 94, 0.35); margin-bottom: 0.8rem; box-sizing: border-box;">
                    1️⃣ Tap Here to Visit Sponsor Link 🔗
                </button>

                <button id="step2-btn" disabled onclick="revealArtwork()" 
                        style="width: 100%; background: #334155; color: #64748b; font-weight: 800; font-size: 1.1rem; padding: 1rem; border-radius: 12px; border: none; cursor: not-allowed; transition: all 0.2s ease; box-sizing: border-box;">
                    🔒 Step 2: Reveal Artwork (Locked)
                </button>
            </div>

            <script>
                function openAdAndUnlock() {{
                    // 1. Open Adsterra direct link
                    window.open('{ADSTERRA_DIRECT_LINK}', '_blank');
                    
                    // 2. Instantly unlock Step 2
                    var btn2 = document.getElementById('step2-btn');
                    btn2.disabled = false;
                    btn2.style.background = 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)';
                    btn2.style.color = '#ffffff';
                    btn2.style.cursor = 'pointer';
                    btn2.innerHTML = '2️⃣ Tap to Reveal Artwork ✨';
                }}

                function revealArtwork() {{
                    // Reload top frame with unlocked parameter
                    window.top.location.href = window.top.location.pathname + '?unlocked=true';
                }}
            </script>
            """,
            height=160
        )

    else:
        # Read image from disk and show
        with open("temp_art.png", "rb") as file:
            img_bytes = file.read()
            st.image(img_bytes, caption=st.session_state.current_caption, use_container_width=True)
            st.download_button(
                label="📥 Download High-Res Image",
                data=img_bytes,
                file_name="pixelforge_artwork.png",
                mime="image/png"
            )
 
