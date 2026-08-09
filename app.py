import streamlit as st
import urllib.parse
import requests

# 1. Page Config & Title
st.set_page_config(page_title="AI Image Generator", page_icon="🎨")
st.title("🎨 AI Image Generator")
st.write("Type a prompt below to create artwork instantly for free!")

# 2. User Input Fields
prompt = st.text_input("What do you want to create?", placeholder="A futuristic city at night, neon lights")
style = st.selectbox("Select a style:", ["None", "Cyberpunk", "Anime", "Photorealistic", "Oil Painting", "3D Render"])

# 3. Generate Button Logic
if st.button("✨ Generate Image", type="primary"):
    if prompt.strip():
        with st.spinner("Generating your image... please wait..."):
            # Format prompt and style
            full_prompt = prompt if style == "None" else f"{prompt}, {style} style"
            encoded_prompt = urllib.parse.quote(full_prompt)
            
            # Direct image server URL
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
            }
            
            try:
                response = requests.get(image_url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    st.image(response.content, caption=f"Prompt: {full_prompt}", use_container_width=True)
                    st.success("Image generated successfully!")
                else:
                    st.error("The server is busy right now. Please try again in a few seconds.")
            except Exception as e:
                st.error(f"Error generating image: {e}")
    else:
        st.warning("Please enter a description first!")
