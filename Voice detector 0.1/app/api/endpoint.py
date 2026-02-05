from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from app.services.audio_engine import AudioProcessor
from app.services.inference import InferenceService

router = APIRouter()
processor = AudioProcessor()
inference = InferenceService()

# --- THE SCHEMA GUVI-HCL EXPECTS ---
class DetectionRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64_format: str # This is the long base64 string

@router.post("/detect")
async def detect_voice(
    request: DetectionRequest, 
    x_api_key: str = Header(None) # GUVI expects the key in this header
):
    # 1. SECURITY CHECK (Optional: Remove if you want it public)
    # If you want to use the key 'my-hackathon-key-2024'
    # if x_api_key != "my-hackathon-key-2024":
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # 2. PROCESS using the new key 'audio_base64_format'
        tensor = processor.process_base64_audio(request.audio_base64_format)
        
        # 3. INFERENCE
        label, score = inference.predict(tensor)
        
        # 4. RESPONSE (Must be JSON)
        return {
            "prediction": label,
            "confidence": score,
            "received_format": request.audio_format,
            "received_language": request.language
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"API Error: {str(e)}")