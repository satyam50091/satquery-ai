from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from database import load_chats, save_chat
from geospatial import extract_metadata
from gemini_service import analyze_with_gemini

# Explicitly defining 'app' so uvicorn can find it
app = FastAPI(title="SatQuery AI Backend")

# Enable CORS so your HTML frontend can communicate with this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/api/chats")
def get_chats():
    return {"chats": load_chats()}

@app.post("/api/analyze")
async def analyze_query(prompt: str = Form(...), file: UploadFile = File(None)):
    file_path = None
    
    if file:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
    # If it's a GeoTIFF or image, we can extract spatial metadata
    spatial_info = None
    if file_path and file.filename.endswith(('.tif', '.tiff')):
        spatial_info = extract_metadata(file_path)

    # Call Gemini
    ai_result = analyze_with_gemini(prompt, file_path)

    # Save chat title to history if it's a new conversation
    save_chat(prompt[:30] + "...")

    return {
        "status": "success",
        "spatial_metadata": spatial_info,
        "ai_analysis": ai_result
    }