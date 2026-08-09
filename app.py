import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

st.set_page_config(page_title="AI Image Generator", page_icon="🎨")

# --- 1. DISPLAY TOP AD BANNER ---
ad_code_top = """
<div style="text-align:center; padding: 10px;">
    <!-- Paste your AdSense or Ad Network Script Here -->
    <p style="color: gray; font-size: 12px;">Advertisement</p>
    <iframe src="https://via.placeholder.com/728x90.png?text=Your+Banner+Ad+Here" width="100%" height="90" frameborder="0"></iframe>
</div>
"""
components.html(ad_code_top, height=110)

# --- 2. APP LOGIC ---
st.title("🎨 AI Image Generator")

prompt = st.text_input("What do you want to create?", placeholder="A cyberpunk street at night")

if st.button("✨ Generate Image", type="primary"):
    if prompt.strip():
        with st.spinner("Generating..."):
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
            response = requests.get(image_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                st.image(response.content, use_container_width=True)
            else:
                st.error("Server busy.")

# --- 3. SIDEBAR AD BANNER ---
with st.sidebar:
    st.write("### Sponsored")
    sidebar_ad = """
    <div style="text-align:center;">
        <iframe src="https://via.placeholder.com/300x250.png?text=Sidebar+Ad" width="100%" height="250" frameborder="0"></iframe>
    </div>
    """
    components.html(sidebar_ad, height=270)
