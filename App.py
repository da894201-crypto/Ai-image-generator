import urllib.parse
import requests
import webbrowser

print("=== AI Image Generator ===")
prompt = input("Enter what you want to create: ")
style = input("Enter a style (e.g. Cyberpunk, Anime, Photorealistic) or press Enter to skip: ")

if style.strip():
    full_prompt = f"{prompt}, {style} style"
else:
    full_prompt = prompt

print("\nGenerating your image... please wait...")

encoded_prompt = urllib.parse.quote(full_prompt)
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
}

try:
    response = requests.get(image_url, headers=headers, timeout=30)
    
    if response.status_code == 200 and "image" in response.headers.get("Content-Type", "").lower():
        # Save the file locally
        filename = "ai_generated_image.png"
        with open(filename, "wb") as file:
            file.write(response.content)
            
        print("\nSuccess! Opening your image in your browser now...")
        
        # Opens your generated photo directly in your browser!
        webbrowser.open(image_url)
    else:
        print(f"\nCould not fetch image. Server code: {response.status_code}")

except Exception as e:
    print(f"\nAn error occurred: {e}")
