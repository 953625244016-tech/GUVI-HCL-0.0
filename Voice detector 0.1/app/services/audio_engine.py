import base64
import io
import librosa
import numpy as np
import torch
from app.core.config import settings

class AudioProcessor:
    # app/services/audio_engine.py

 def process_base64_audio(self, b64_string: str):
    try:
        # 1. Catch empty strings (The most common honeypot test)
        if not b64_string or len(b64_string) < 10:
            raise ValueError("Empty signal")

        if "," in b64_string:
            b64_string = b64_string.split(",")[1]
            
        # 2. Safe Base64 decoding
        try:
            audio_bytes = base64.b64decode(b64_string)
        except:
            raise ValueError("Invalid Base64 encoding")

        # 3. Safe Audio Loading
        buffer = io.BytesIO(audio_bytes)
        try:
            y, sr = librosa.load(buffer, sr=settings.SAMPLE_RATE)
        except:
            raise ValueError("Could not decode audio codec")
            
        # ... (rest of your LightCNN processing)
        
    except Exception as e:
        # Log error to terminal and re-raise for the global handler
        print(f"Honeypot Blocked: {str(e)}")
        raise ValueError(str(e))