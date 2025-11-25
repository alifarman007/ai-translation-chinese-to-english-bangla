# Indonesian Voice Translator (index_3.html)

Complete voice translation system supporting Indonesian, Bangla, and English with automatic language detection and WhatsApp sharing.

## Features

### Supported Translation Directions

1. **Bangla → Indonesian**
2. **English → Indonesian**
3. **Indonesian → Bangla**
4. **Indonesian → English**

### Auto-Detection

When translating **to Indonesian**, the system can automatically detect whether the source is Bangla or English:
- No need to manually select the source language
- Just enable "Auto-detect language" checkbox
- Speak in either Bangla or English
- System will detect and translate to Indonesian

### WhatsApp Sharing

- Share both translation text and audio to WhatsApp
- **Mobile**: Uses Web Share API to share text + audio file together
- **Desktop**: Downloads audio + opens WhatsApp Web with text
- Works seamlessly on all devices

## How to Use

### 1. Access the Page
```
http://localhost:8000/static/index_3.html
```

### 2. Select Language Mode

**Option A: Manual Selection**
1. Click on source language button (Bangla, English, or Indonesian)
2. Target language updates automatically
3. Record and translate

**Option B: Auto-Detection (for Indonesian translation)**
1. Keep Indonesian selected as source
2. Check "Auto-detect language (Bangla/English)"
3. Speak in either Bangla or English
4. System detects language and translates to Indonesian

### 3. Record & Translate

1. Press and hold the microphone button
2. Speak clearly in your selected language
3. Release button when finished
4. Translation appears with audio playback

### 4. Share to WhatsApp

1. After translation completes
2. Click "Share to WhatsApp" button
3. Select contact and send (text + audio)

## Translation Examples

### Bangla → Indonesian
```
Input (Bangla): আমি ভালো আছি
Output (Indonesian): Saya baik-baik saja
```

### English → Indonesian
```
Input (English): How are you?
Output (Indonesian): Apa kabar?
```

### Indonesian → Bangla
```
Input (Indonesian): Selamat pagi
Output (Bangla): সুপ্রভাত
```

### Indonesian → English
```
Input (Indonesian): Terima kasih
Output (English): Thank you
```

## Technical Details

### Backend Support

**1. Speech-to-Text** (`src/speech_to_text.py`)
- Added `id-ID` (Indonesian - Indonesia) to language detection
- Supports auto-detection among: Bangla, English, Chinese, Indonesian
- Uses confidence scores to pick best match

**2. Translation** (`src/translator.py`)
- Added Indonesian language mapping
- Supports `id` and `id-ID` language codes
- Google Translate API handles all translation pairs

**3. Text-to-Speech** (`src/text_to_speech.py`)
- Added Indonesian voice: `id-ID-Standard-A`
- Female standard voice for Indonesian
- High-quality audio synthesis

### Frontend Features

**1. Language Selection**
- 3 source language buttons (Bangla, English, Indonesian)
- Auto-detect checkbox for Bangla/English → Indonesian
- Dynamic target language display

**2. Auto-Detection**
- Only available when source is NOT Indonesian
- Tries both Bangla and English
- Picks best match based on confidence

**3. UI/UX**
- Mobile-friendly responsive design
- Red to teal gradient theme
- Smooth animations and transitions
- Clear status messages
- Touch-optimized buttons

## Mobile Optimization

### Responsive Design
- Adapts to all screen sizes
- Touch-friendly button sizes
- Optimized font sizes for mobile
- Proper viewport configuration

### Recording
- Press and hold to record
- Visual feedback during recording
- Prevents accidental context menu on long press

### Audio Playback
- Automatic playback after translation
- Fallback for browsers that block autoplay
- Tap anywhere to play if blocked

## Browser Compatibility

### Desktop
- Chrome: ✓ Full support
- Firefox: ✓ Full support
- Safari: ✓ Full support
- Edge: ✓ Full support

### Mobile
- Chrome (Android): ✓ Full support + Web Share API
- Safari (iOS): ✓ Full support + Web Share API
- Firefox Mobile: ✓ Full support (text-only WhatsApp share)

## API Integration

The page uses the existing `/translate-voice` endpoint:

**Request:**
```javascript
formData.append('file', audioFile);
formData.append('source_language', 'id');  // Indonesian
formData.append('target_languages', 'bn'); // Bangla
```

**Response:**
```json
{
  "success": true,
  "transcription": {
    "text": "Selamat pagi",
    "confidence": 0.95,
    "language": "id-ID"
  },
  "translations": {
    "bangla": "সুপ্রভাত"
  },
  "audio_files": {
    "bangla": {
      "url": "/outputs/audio_bn_20250125_123456.mp3",
      "size_kb": 15.2
    }
  }
}
```

## Files Modified

### New Files
- `static/index_3.html` - Indonesian translator interface

### Updated Files
- `src/translator.py` - Added Indonesian language mappings
- `src/text_to_speech.py` - Added Indonesian voice support
- `src/speech_to_text.py` - Added Indonesian to auto-detection

### No Changes Required
- `main.py` - Uses existing API endpoints
- `src/pipeline.py` - Works with all languages automatically

## Testing

### Test All Translation Directions

**1. Bangla → Indonesian**
```bash
# Open: http://localhost:8000/static/index_3.html
# Click: Bangla button
# Record: "আমি তোমাকে ভালোবাসি"
# Verify: Indonesian translation appears
```

**2. English → Indonesian**
```bash
# Click: English button
# Record: "I love you"
# Verify: Indonesian translation appears
```

**3. Indonesian → Bangla**
```bash
# Click: Indonesian button
# Record: "Aku cinta kamu"
# Verify: Bangla translation appears
```

**4. Indonesian → English**
```bash
# Click: Indonesian button (target will be English)
# Record: "Selamat tinggal"
# Verify: English translation appears
```

**5. Auto-Detect → Indonesian**
```bash
# Enable: Auto-detect checkbox
# Record in Bangla: "হ্যালো"
# Verify: Indonesian translation + "detected" label
# OR
# Record in English: "Hello"
# Verify: Indonesian translation + "detected" label
```

### Test WhatsApp Share

**On Mobile:**
1. Complete a translation
2. Click "Share to WhatsApp"
3. Verify share sheet opens
4. Select WhatsApp
5. Verify text + audio shared

**On Desktop:**
1. Complete a translation
2. Click "Share to WhatsApp"
3. Verify audio downloads
4. Verify WhatsApp Web opens
5. Manually attach downloaded audio

## Troubleshooting

### Translation Not Working
- Check server is running: `python3 main.py`
- Check console for errors (F12)
- Verify GOOGLE_API_KEY in .env

### Audio Not Playing
- Check browser console for errors
- Try clicking anywhere to trigger playback
- Check browser autoplay settings

### WhatsApp Share Not Working
- **Mobile**: Ensure browser supports Web Share API
- **Desktop**: Check if audio downloaded properly
- Check browser console for errors

### Auto-Detect Not Working
- Ensure checkbox is enabled
- Speak clearly and louder
- Try longer phrases (3-5 words minimum)
- Check if language is actually Bangla or English

## Notes

- Indonesian TTS uses Google's standard voice (high quality)
- Auto-detection works best with clear audio and longer phrases
- WhatsApp sharing requires HTTPS in production (works on localhost)
- All audio files are automatically cleaned up after sharing
- Maximum audio file size: 10MB

## Future Enhancements

Potential improvements:
- Add more Indonesian dialects
- Support Javanese and Sundanese
- Add voice gender selection
- Add speaking rate control
- Add pronunciation guide
- Support text input mode
- Add translation history
