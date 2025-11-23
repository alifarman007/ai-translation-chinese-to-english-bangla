#!/bin/bash

# Test script for /speech-to-text API endpoint using cURL
# Usage: ./test_speech_to_text_curl.sh <audio_file_path>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <audio_file_path>"
    echo ""
    echo "Example:"
    echo "  $0 uploads/test.mp3"
    echo "  $0 uploads/english.wav"
    echo ""
    echo "Language auto-detection:"
    echo "  The API automatically detects language among:"
    echo "  - Chinese (Mandarin)"
    echo "  - English"
    echo "  - Bangla"
    exit 1
fi

AUDIO_FILE=$1

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: File not found: $AUDIO_FILE"
    exit 1
fi

echo "Testing /speech-to-text endpoint"
echo "File: $AUDIO_FILE"
echo "Language: Auto-detection (Chinese, English, Bangla)"
echo "Sending request to: http://localhost:8000/speech-to-text"
echo "------------------------------------------------------------"

curl -X POST "http://localhost:8000/speech-to-text" \
  -F "file=@$AUDIO_FILE" \
  -H "accept: application/json" | jq .

echo ""
echo "Done!"
