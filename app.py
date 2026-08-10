import streamlit as st
import urllib.parse
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PixelForge AI - Instant Art Generator",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)

PRO_PASSWORD = "UNLIMITED2026"

# 🔴 REPLACE THIS WITH YOUR ACTIVE ADSTERRA DIRECT LINK 🔴
ADSTERRA_DIRECT_LINK ="https://www.effectivecpmnetwork.com/vqwptfhf7e?key=387fee6ebf196f7838452f5a26520fb4"

# --- CUSTOM MODERN CSS STYLING ---
st.markdown("""
<style>
    /* Premium Background */
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 60%, #090d16 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Hide Instruction Hints */
    div[data-testid="stWidgetInstructions"], 
    small[data-testid="stWidgetInstructions"],
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Main Header Styling */
    .header-box {
        text-align: center;
        padding: 2.2rem 1.2rem 1.2rem 1.2rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.8rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }

    /* Glassmorphism Card Container */
    .card-box {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        padding: 1.6rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
    }

    /* Styled Input Fields & Dropdowns */
    div[data-baseweb="input"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #ffffff !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #ffffff !important;
    }

    /* Field Labels */
    label {
        font-weight: 600 !important;
        letter-spacing: 0.3px;
        color: #cbd5e1 !important;
    }

    /* Modern Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 0.75rem 1.2rem !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(99, 102, 241, 0.45) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
    }

    /* Step 1 Ad Button Styling */
    .ad-step1-btn {
        display: block;
        width: 100%;
        text-align: center;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: #ffffff !important;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 0.95rem;
        border-radius: 12px;
        text-decoration: none !important;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.35);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }

    .ad-step1-btn:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0f19 0%, #05070d 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .sidebar-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
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
        font-weight: 600;
        font-size: 0.95rem;
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
if "is_locked" not in st.session_state:
    st.session_state.is_locked = False

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
        <img src="https://img.icons8.com/3d-fluency/94/sparkles.png" width="55" style="margin-bottom: 8px;">
        <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #a855f7, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PixelForge Pro</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.is_pro:
        st.markdown("""
        <div class="sidebar-card" style="border-color: rgba(34, 197, 94, 0.4); background: rgba(34, 197, 94, 0.08); text-align: center;">
            <div style="color: #4ade80; font-weight: 800; font-size: 1.05rem;">🌟 PRO ACTIVE</div>
            <div style="color: #94a3b8; font-size: 0.82rem; margin-top: 4px;">Unlimited Generations • No Ads</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="credit-badge">
            <span>⚡ Free Credits</span>
            <span style="background: #6366f1; color: #ffffff; padding: 3px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 700;">{st.session_state.generations_left} Left</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-weight: 700; font-size: 0.95rem; color: #f1f5f9; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 6px;">
            🔑 Unlock Pro Access
        </div>
        """, unsafe_allow_html=True)
        
        passcode_input = st.text_input("Passcode", type="password", key="sidebar_passcode_input", label_visibility="collapsed", placeholder="Enter passcode...")
        
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Activate Passcode", key="sidebar_passcode_btn"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro status unlocked!")
                st.rerun()
            else:
                st.error("Invalid key.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN APP HEADER ---
st.markdown("""
<div class="header-box">
    <div class="header-title">🎨 PixelForge AI</div>
    <p style="color: #94a3b8; font-size: 1.05rem; margin: 0;">Transform text prompts into stunning artwork in seconds</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN INPUT CARD ---
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
                            st.session_state.is_locked = True
                        else:
                            st.session_state.is_locked = False
                        st.rerun()
                    else:
                        st.error("Server busy, try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type a description first!")

else:
    st.markdown("""
    <div class="card-box" style="border: 1px solid #ef4444; text-align: center;">
        <h2 style="color: #ef4444; margin-top: 0;">🔒 Free Credits Exhausted</h2>
        <p style="color: #cbd5e1;">You've used all 3 free image generations.</p>
        <p>Subscribe to Pro for <b>instant generations</b>, <b>zero ad breaks</b>, and <b>unlimited high-res downloads</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("[👉 **Click Here to Subscribe for $5/month on Gumroad**](https://daniel.gumroad.com)")

# --- DISPLAY RESULT ---
if st.session_state.generated_image_bytes:
    st.write("---")
    st.markdown("### 🖼️ Your Generated Artwork")
    
    if st.session_state.is_locked:
        st.markdown("""
        <div class="card-box" style="text-align: center; border: 1px solid #3b82f6;">
            <h3 style="margin-top: 0; color: #60a5fa;">🔓 Image Ready To Unlock</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Complete both steps below to reveal your generated artwork:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 1: Open Adsterra link in new tab (Native HTML link)
        st.markdown(f'''
            <a href="{ADSTERRA_DIRECT_LINK}" target="_blank" class="ad-step1-btn">
                1️⃣ Tap Here to Visit Sponsor Link 🔗
            </a>
        ''', unsafe_allow_html=True)
        
        # Step 2: Native Streamlit Button (Unlocks image state without page reload)
        if st.button("2️⃣ Reveal Generated Artwork ✨", key="native_reveal_btn"):
            st.session_state.is_locked = False
            st.rerun()

    else:
        st.image(st.session_state.generated_image_bytes, caption=st.session_state.current_caption, use_container_width=True)
        st.download_button(
            label="📥 Download High-Res Image",
            data=st.session_state.generated_image_bytes,
            file_name="pixelforge_artwork.png",
            mime="image/png",
            key="download_img_btn"
        )
