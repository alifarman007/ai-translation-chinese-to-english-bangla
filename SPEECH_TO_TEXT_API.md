# Speech-to-Text API

Simple API endpoint for converting speech to text with automatic language detection.

## Endpoint

```
POST /speech-to-text
```

## Features

- **Simple input**: Only requires an audio file
- **Automatic language detection**: Detects among Chinese, English, and Bangla
- **Multiple audio formats**: Supports WAV, MP3, FLAC, WEBM, OGG, MP4, M4A
- **Max file size**: 10MB

## Request

**Parameters:**
- `file` (required): Audio file in any supported format

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/speech-to-text" \
  -F "file=@your_audio.mp3"
```

**Example using Python:**
```python
import requests

with open('your_audio.mp3', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/speech-to-text', files=files)
    result = response.json()
    print(result['text'])
```

**Example using JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', audioFile);

fetch('http://localhost:8000/speech-to-text', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data.text));
```

## Response

**Success (200 OK):**
```json
{
  "success": true,
  "text": "你好世界",
  "confidence": 0.95,
  "language": "zh-CN",
  "processing_time": 1.23,
  "timestamp": "2025-11-23T12:34:56.789"
}
```

**Error (500):**
```json
{
  "message": "Speech-to-text failed",
  "error": "No speech detected",
  "processing_time": 0.45
}
```

**Error (400 - Invalid file):**
```json
{
  "detail": "Invalid file type. Allowed: wav, mp3, flac, webm, ogg, mp4, m4a"
}
```

**Error (413 - File too large):**
```json
{
  "detail": "File too large. Maximum size: 10MB"
}
```

## Testing

### Using the test script (Python):
```bash
python3 test_speech_to_text_api.py uploads/your_audio.mp3
```

### Using the test script (cURL):
```bash
./test_speech_to_text_curl.sh uploads/your_audio.mp3
```

### Using the interactive API docs:
1. Start the server: `python3 main.py`
2. Open browser: `http://localhost:8000/docs`
3. Find the `/speech-to-text` endpoint under "Speech" section
4. Click "Try it out"
5. Upload your audio file
6. Click "Execute"

## Supported Languages

The API automatically detects the language from the audio among:
- **bn-BD**: Bangla (Bangladesh)
- **en-US**: English
- **zh-CN**: Chinese (Mandarin)

## How Language Detection Works

The API tries all three supported languages and automatically selects the one with the highest confidence score. This ensures:
- **Bangla audio** is correctly detected as Bangla (not misidentified as Chinese)
- **English audio** is correctly detected as English
- **Chinese audio** is correctly detected as Chinese

The detection happens automatically - you don't need to specify the language!

## Notes

- Language detection is automatic - no need to specify the language
- The API tries all supported languages (Bangla, English, Chinese) and picks the best match
- Uses confidence scores to determine the correct language
- The API uses Google Speech-to-Text with optimized settings for speech recognition
- Audio files are automatically optimized (mono, 16kHz) if FFmpeg is available
- Uploaded files are automatically cleaned up after processing
- Note: Since the API tries multiple languages, processing may take slightly longer but ensures accurate language detection
