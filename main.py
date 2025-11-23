from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from datetime import datetime
import traceback
from src.pipeline import TranslationPipeline

# Initialize FastAPI app
app = FastAPI(
    title="Multilingual Translation API",
    description="Bidirectional translation between Chinese, English, and Bangla with speech-to-text and text-to-speech",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'webm', 'ogg', 'mp4', 'm4a'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Initialize pipeline
pipeline = None

@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup"""
    global pipeline
    try:
        pipeline = TranslationPipeline()
        print("✓ Translation pipeline initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize pipeline: {e}")
        pipeline = None


# Pydantic models for request/response
class TranslateTextRequest(BaseModel):
    text: str
    source_language: Optional[str] = "zh-CN"
    target_languages: Optional[list] = ["en", "bn"]
    generate_audio: Optional[bool] = True


class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/", tags=["Info"])
async def root():
    """Serve the web interface"""
    return FileResponse('static/index.html')


@app.get("/api", tags=["Info"])
async def api_info():
    """API information"""
    return {
        "service": "Multilingual Translation API (Chinese ⇄ English ⇄ Bangla)",
        "version": "2.0.0",
        "status": "running",
        "documentation": "/docs",
        "supported_languages": {
            "zh-CN": "Chinese (Mandarin)",
            "en": "English",
            "bn": "Bangla"
        },
        "endpoints": {
            "POST /translate-voice": "Upload audio for bidirectional translation",
            "POST /translate-text": "Translate text in any direction",
            "POST /speech-to-text": "Convert speech to text only (no translation)",
            "GET /health": "Check API health",
            "GET /download/{filename}": "Download generated audio files"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Pipeline not initialized"
        )
    
    return {
        "status": "healthy",
        "message": "All systems operational",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/translate-voice", tags=["Translation"])
async def translate_voice(
    file: UploadFile = File(...),
    source_language: Optional[str] = Form("zh-CN"),
    target_languages: Optional[str] = Form("en,bn")
):
    """
    Upload audio file and get translations with audio outputs

    **Parameters:**
    - **file**: Audio file (WAV, MP3, FLAC, WEBM, OGG, MP4, M4A) - Max 10MB
    - **source_language**: Source language code (default: zh-CN for Chinese; also supports en, bn)
    - **target_languages**: Comma-separated target language codes (default: en,bn; supports en, bn, zh)

    **Returns:**
    - Transcription of original audio
    - Translations to target languages
    - URLs to download generated audio files
    - Processing time and metadata
    """
    
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Translation pipeline not initialized"
        )
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{timestamp}_upload.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            os.remove(file_path)
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        print(f"[API] File uploaded: {unique_filename} ({file_size / 1024:.2f} KB)")

        # Parse target languages
        target_langs = [lang.strip() for lang in target_languages.split(',')]

        # Process through pipeline
        result = pipeline.process_audio(
            audio_file_path=file_path,
            source_language=source_language,
            target_languages=target_langs
        )
        
        # Prepare response
        if result['success']:
            response = {
                "success": True,
                "transcription": {
                    "text": result['transcription']['text'],
                    "confidence": result['transcription']['confidence'],
                    "language": result['transcription']['language']
                },
                "translations": {},
                "audio_files": {},
                "processing_time": result['processing_time'],
                "timestamp": result['timestamp']
            }
            
            # Add translations
            for lang_name, translation in result['translations'].items():
                if translation['success']:
                    response['translations'][lang_name] = translation['text']
            
            # Add audio file URLs
            for lang_name, audio_info in result['audio_outputs'].items():
                if audio_info['success']:
                    audio_filename = os.path.basename(audio_info['audio_path'])
                    response['audio_files'][lang_name] = {
                        "url": f"/outputs/{audio_filename}",
                        "size_kb": audio_info['file_size']
                    }
            
            print(f"[API] ✓ Translation successful (Time: {result['processing_time']:.2f}s)")
            
            return JSONResponse(content=response, status_code=200)
        
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Translation pipeline failed",
                    "errors": result['errors'],
                    "processing_time": result['processing_time']
                }
            )
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"[API] ✗ Error: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@app.post("/translate-text", tags=["Translation"])
async def translate_text(request: TranslateTextRequest):
    """
    Translate text directly (without audio input)

    **Request Body:**
```json
    {
        "text": "hello world",
        "source_language": "en",
        "target_languages": ["zh"],
        "generate_audio": true
    }
```

    **Returns:**
    - Translations to target languages
    - URLs to download generated audio (if generate_audio=true)
    """
    
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Translation pipeline not initialized"
        )
    
    try:
        text = request.text
        source_language = request.source_language
        target_languages = request.target_languages
        generate_audio = request.generate_audio

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Text field cannot be empty"
            )

        print(f"[API] Translating text: {text[:50]}...")
        print(f"[API] Source: {source_language}, Targets: {target_languages}")

        # Translate
        translation_result = pipeline.translator.translate_to_multiple(
            text,
            target_languages=target_languages,
            source_language=source_language
        )
        
        response = {
            "success": True,
            "original_text": text,
            "translations": {},
            "audio_files": {}
        }
        
        # Add translations
        for lang_name, translation in translation_result['translations'].items():
            if translation['success']:
                response['translations'][lang_name] = translation['text']
        
        # Generate audio if requested
        if generate_audio:
            tts_result = pipeline.tts.synthesize_multiple(translation_result['translations'])
            
            for lang_name, audio_info in tts_result['audio_files'].items():
                if audio_info['success']:
                    audio_filename = os.path.basename(audio_info['audio_path'])
                    response['audio_files'][lang_name] = {
                        "url": f"/outputs/{audio_filename}",
                        "size_kb": audio_info['file_size']
                    }
        
        print(f"[API] ✓ Text translation successful")
        
        return JSONResponse(content=response, status_code=200)
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"[API] ✗ Error: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@app.post("/speech-to-text", tags=["Speech"])
async def speech_to_text(
    file: UploadFile = File(...)
):
    """
    Convert speech to text (supports any audio format)

    **Parameters:**
    - **file**: Audio file in any format (WAV, MP3, FLAC, WEBM, OGG, MP4, M4A) - Max 10MB

    **Returns:**
    - Transcribed text
    - Confidence score
    - Language detected
    - Processing metadata

    **Note:** Language is automatically detected from the audio
    """

    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Translation pipeline not initialized"
        )

    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{timestamp}_stt.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            os.remove(file_path)
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
            )

        print(f"[API] Speech-to-text file uploaded: {unique_filename} ({file_size / 1024:.2f} KB)")

        # Process through speech-to-text with automatic language detection
        start_time = datetime.now()
        stt_result = pipeline.stt.transcribe_audio(file_path, language_code=None)
        processing_time = (datetime.now() - start_time).total_seconds()

        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass

        # Prepare response
        if stt_result['success']:
            response = {
                "success": True,
                "text": stt_result['transcription'],
                "confidence": stt_result['confidence'],
                "language": stt_result['language'],
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat()
            }

            print(f"[API] ✓ Speech-to-text successful (Time: {processing_time:.2f}s)")

            return JSONResponse(content=response, status_code=200)

        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Speech-to-text failed",
                    "error": stt_result['error'],
                    "processing_time": processing_time
                }
            )

    except HTTPException:
        raise

    except Exception as e:
        print(f"[API] ✗ Error: {str(e)}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@app.get("/download/{filename}", tags=["Files"])
async def download_file(filename: str):
    """
    Download generated audio files

    **Parameters:**
    - **filename**: Name of the audio file to download

    **Returns:**
    - Audio file (MP3 format)
    """
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Download error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 MULTILINGUAL TRANSLATION API SERVER (FastAPI)")
    print("="*60)
    print("Bidirectional: Chinese ⇄ English ⇄ Bangla")
    print("Features: Speech-to-Text, Translation, Text-to-Speech")
    print("Server starting...")
    print("Web Interface: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("="*60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )