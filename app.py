import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests
import time

st.set_page_config(page_title="AI Image Generator", page_icon="🎨", layout="centered")

PRO_PASSWORD = "UNLIMITED2026"

# 1. Initialize State
if "generations_left" not in st.session_state:
    st.session_state.generations_left = 3
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# 2. Sidebar Passcode System
with st.sidebar:
    st.header("⚙️ Account Status")
    if st.session_state.is_pro:
        st.success("🌟 Pro Member (Instant Generation & No Ads)")
    else:
        st.info(f"⚡ Free Plan: **{st.session_state.generations_left} left**")
        st.write("---")
        st.subheader("Already Subscribed?")
        passcode_input = st.text_input("Enter Pro Access Key:", type="password")
        if st.button("Unlock Unlimited"):
            if passcode_input == PRO_PASSWORD:
                st.session_state.is_pro = True
                st.success("Access unlocked!")
                st.rerun()
            else:
                st.error("Invalid access key.")

# 3. Main Interface
st.title("🎨 AI Image Generator")
prompt = st.text_input("What do you want to create?", placeholder="A futuristic city at night")
style = st.selectbox("Select a style:", ["None", "Cyberpunk", "Anime", "Photorealistic", "3D Render"])

can_generate = st.session_state.is_pro or st.session_state.generations_left > 0

if can_generate:
    if st.button("✨ Generate Image", type="primary"):
        if prompt.strip():
            # Step A: Fetch the image behind the scenes
            full_prompt = prompt if style == "None" else f"{prompt}, {style} style"
            encoded_prompt = urllib.parse.quote(full_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
            
            try:
                response = requests.get(image_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    
                    # Step B: If FREE user, force the 10-second unskippable ad timer
                    if not st.session_state.is_pro:
                        st.warning("📺 Free Generation: Please view the sponsor ad below while your image renders...")
                        
                        # --- UNSKIPPABLE AD DISPLAY ---
                        ad_code = """
                        <div style="text-align:center; padding: 10px; border: 2px solid #ff4b4b; border-radius: 10px; background-color: #111;">
                            <p style="color: #ff4b4b; font-weight: bold; margin-bottom: 5px;">SPONSORED ADVERTISEMENT</p>
                            <!-- Replace with your actual HTML/JS ad code from Adsterra/Network -->
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
                        components.html(ad_code, height=290)
                        
                        # Live Countdown Timer Bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        wait_seconds = 10
                        for i in range(wait_seconds):
                            time.sleep(1)
                            percent_complete = int(((i + 1) / wait_seconds) * 100)
                            progress_bar.progress(percent_complete)
                            status_text.text(f"⏳ Unlocking image in {wait_seconds - (i + 1)} seconds...")
                        
                        status_text.empty()
                        progress_bar.empty()
                    
                    # Step C: Show Image and Deduct Credit
                    st.image(response.content, use_container_width=True)
                    
                    if not st.session_state.is_pro:
                        st.session_state.generations_left -= 1
                        st.rerun()

                else:
                    st.error("Server busy, try again.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a description.")

else:
    # 4. Paywall Screen
    st.error("🔒 You've used all 3 free generations!")
    st.info("Subscribe to skip ads and get instant, unlimited generations!")
    st.markdown("### [👉 **Click Here to Subscribe for $5/month**](https://daniel.gumroad.com)")
