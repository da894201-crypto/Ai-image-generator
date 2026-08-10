import streamlit as st
import urllib.parse
import requests
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PixelForge AI",
    page_icon="🎨",
    layout="centered"
)

PRO_PASSWORD = "UNLIMITED2026"
ADSTERRA_DIRECT_LINK = "https://www.effectivecpmnetwork.com/1e3820839b36df037dab169eee1f0358"

# --- SESSION STATE INITIALIZATION ---
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False
if "current_caption" not in st.session_state:
    st.session_state.current_caption = ""
if "is_locked" not in st.session_state:
    st.session_state.is_locked = False
if "step1_activated" not in st.session_state:
    st.session_state.step1_activated = False

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎨 PixelForge Pro")
    if st.session_state.is_pro:
        st.success("🌟 PRO UNLOCKED")
    else:
        st.write(f"⚡ Free Credits Left: **{st.session_state.generations_left}**")
        passcode = st.text_input("Passcode", type="password")
        if st.button("Activate Pro"):
            if passcode == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Pro activated!")
                st.rerun()
            else:
                st.error("Incorrect passcode")

# --- MAIN UI ---
st.title("🎨 PixelForge AI")
st.write("Transform your text prompts into stunning artwork instantly.")

prompt = st.text_input("Prompt:", placeholder="e.g., A futuristic cybernetic knight")
style = st.selectbox("Style:", ["None", "Cyberpunk", "Anime", "Photorealistic", "Fantasy"])
aspect_ratio = st.selectbox("Ratio:", ["Square (1:1)", "Portrait (3:4)", "Landscape (16:9)"])

can_generate = st.session_state.is_pro or st.session_state.generations_left > 0

if can_generate:
    if st.button("✨ Generate Artwork", type="primary"):
        if prompt.strip():
            with st.spinner("Rendering artwork (this can take up to a minute)..."):
                full_prompt = prompt if style == "None" else f"{prompt}, {style} style"
                encoded_prompt = urllib.parse.quote(full_prompt)
                
                width, height = 1024, 1024
                if aspect_ratio == "Portrait (3:4)":
                    width, height = 768, 1024
                elif aspect_ratio == "Landscape (16:9)":
                    width, height = 1024, 576
                
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                headers = {"User-Agent": "Mozilla/5.0"}
                
                try:
                    response = requests.get(image_url, headers=headers, timeout=60)
                    if response.status_code == 200:
                        with open("temp_art.png", "wb") as f:
                            f.write(response.content)
                        
                        st.session_state.current_caption = f"\"{full_prompt}\""
                        
                        if not st.session_state.is_pro:
                            st.session_state.generations_left -= 1
                            st.session_state.is_locked = True
                            st.session_state.step1_activated = False
                        st.rerun()
                    else:
                        st.error("Server busy, please try clicking generate again.")
                except requests.exceptions.Timeout:
                    st.error("The image generation server took too long to respond. Please try clicking generate again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt!")

# --- DISPLAY RESULT & LOCK SYSTEM ---
if os.path.exists("temp_art.png"):
    st.divider()
    st.subheader("🖼️ Your Generated Artwork")
    
    if st.session_state.is_locked:
        st.info("🔓 **Image Locked:** Complete the steps below to unlock your creation:")
        
        # Step 1: User must click this button first to unlock Step 2
        if not st.session_state.step1_activated:
            if st.button("1️⃣ Tap Here to Prepare Sponsor Link", use_container_width=True):
                st.session_state.step1_activated = True
                st.rerun()
        else:
            # Step 2: Only reveals itself AFTER Step 1 has been clicked
            st.link_button("🔗 Click Here to Open Sponsor Page", ADSTERRA_DIRECT_LINK, use_container_width=True)
            
            st.write("")
            
            if st.button("2️⃣ Verify & Unlock Artwork ✨", type="primary", use_container_width=True):
                with st.spinner("Verifying sponsor visit... Please wait 5 seconds."):
                    time.sleep(5)
                st.session_state.is_locked = False
                st.session_state.step1_activated = False
                st.rerun()
    else:
        with open("temp_art.png", "rb") as file:
            img_bytes = file.read()
            st.image(img_bytes, caption=st.session_state.current_caption, use_container_width=True)
            st.download_button(
                label="📥 Download High-Res Image",
                data=img_bytes,
                file_name="pixelforge_artwork.png",
                mime="image/png",
                use_container_width=True
            )
