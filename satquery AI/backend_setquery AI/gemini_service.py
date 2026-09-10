import os
import google.generativeai as genai

# Configure your Gemini API key (Make sure to set your environment variable or paste key)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE"))

def analyze_with_gemini(prompt: str, image_path: str = None):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        
        if image_path and os.path.exists(image_path):
            # Upload file to Gemini File API if it's an image/map
            sample_file = genai.upload_file(path=image_path)
            response = model.generate_content([sample_file, prompt])
        else:
            response = model.generate_content(prompt)
            
        return {"success": True, "response": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}