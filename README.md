# Chinese to English and Bangla Translation System

A full-stack translation system that converts Chinese voice input to English and Bangla, with both text and audio output. Built with FastAPI and Google Cloud APIs.

## Overview

This application provides automatic translation of Chinese (Mandarin) audio to English and Bangla. Users can upload audio files or record directly through their browser. The system transcribes the Chinese speech, translates it to both target languages, and generates natural-sounding audio output.

## Key Features

- Speech-to-Text conversion for Chinese audio
- Simultaneous translation to English and Bangla
- Text-to-Speech audio generation in both languages
- Web interface with file upload and voice recording
- Audio playback and download functionality
- REST API with automatic documentation

## Technology Stack

**Backend:**
- Python
- FastAPI web framework
- Google Cloud Speech-to-Text API
- Google Cloud Translation API
- Google Cloud Text-to-Speech API

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive web design
- Web Audio API for playback
- MediaRecorder API for recording

## Installation

### Prerequisites

- Python
- Google Cloud account
- API key with enabled services (Speech-to-Text, Translation, Text-to-Speech)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/alifarman007/ai-translation-chinese-to-english-bangla.git
cd ai-translation-chinese-to-english-bangla
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your credentials:
```
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id
```

5. Start the server:
```bash
python main.py
```

6. Open your browser at `http://localhost:8000`

## Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Upload a Chinese audio file or click "Start Recording"
3. Click "Translate" to process
4. View translations and play/download audio files

### API Endpoints

**POST /translate-voice**
Upload audio file for translation
```bash
curl -X POST http://localhost:8000/translate-voice -F "file=@audio.mp3"
```

**POST /translate-text**
Translate text without audio input
```bash
curl -X POST http://localhost:8000/translate-text \
  -H "Content-Type: application/json" \
  -d '{"text":"你好世界","generate_audio":true}'
```

**GET /health**
Check API health status

**GET /download/{filename}**
Download generated audio files

Full API documentation available at `http://localhost:8000/docs`

## Project Structure
```
translation-app/
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (not in repo)
├── src/
│   ├── speech_to_text.py  # STT module
│   ├── translator.py       # Translation module
│   ├── text_to_speech.py   # TTS module
│   └── pipeline.py         # Complete pipeline
├── static/
│   └── index.html          # Web interface
├── uploads/                # Temporary file storage
└── outputs/                # Generated audio files
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_cloud_api_key
GOOGLE_CLOUD_PROJECT=your_project_id
```

### Google Cloud Setup

1. Go to Google Cloud Console
2. Create a new project
3. Enable these APIs:
   - Cloud Speech-to-Text API
   - Cloud Translation API
   - Cloud Text-to-Speech API
4. Create an API key in "Credentials"
5. Restrict the key to only these three APIs

## Cost Information

**Free Tier (per month):**
- Speech-to-Text: First 60 minutes
- Translation: First 500,000 characters
- Text-to-Speech: First 4 million characters

**After Free Tier:**
- Approximately $3-5 per hour of processed audio

## Development

### Running Tests

Test individual modules:
```bash
python src/speech_to_text.py
python src/translator.py
python src/text_to_speech.py
python src/pipeline.py
```

### Debug Mode

The application runs with auto-reload in development mode. Changes to Python files will automatically restart the server.

## Limitations

- Maximum file size: 10 MB
- Supported formats: WAV, MP3, FLAC
- Source language: Chinese (Mandarin) only
- Target languages: English and Bangla only
- Requires internet connection

## Troubleshooting

**API Key Issues:**
- Verify key is correct in `.env` file
- Ensure all three APIs are enabled
- Check key restrictions in Google Cloud Console

**Audio Playback Problems:**
- Check browser console for errors (press F12)
- Verify files exist in `outputs/` folder
- Try downloading and playing locally

**Translation Failures:**
- Check Google Cloud quota limits
- Verify internet connection
- Review server logs for detailed errors

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes.

## License

MIT License - see LICENSE file for details

## Contact

Project Link: https://github.com/alifarman007/ai-translation-chinese-to-english-bangla

For issues or questions, please open an issue on GitHub.

## Acknowledgments

- Google Cloud Platform for AI/ML APIs
- FastAPI framework
- Open source community