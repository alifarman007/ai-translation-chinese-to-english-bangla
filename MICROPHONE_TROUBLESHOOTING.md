# Microphone Recording Troubleshooting Guide

## Overview
This guide helps resolve issues with the voice recording feature in the Multilingual Translation webapp.

## Common Issues and Solutions

### 1. "Cannot read properties of undefined (reading 'getUserMedia')"

**Cause**: Browser doesn't support the MediaDevices API or page is not served securely.

**Solutions**:
- ✅ **Use HTTPS or localhost**: The recording API only works on secure contexts (HTTPS) or localhost
- ✅ **Use a modern browser**: Chrome, Firefox, Edge, or Safari (latest versions)
- ✅ **Update your browser**: Make sure you're using the latest version

**How to run locally**:
```bash
# Option 1: Using Python's built-in server (localhost)
python main.py

# Then open: http://localhost:8000
```

### 2. "Permission denied. Please allow microphone access"

**Cause**: Browser blocked microphone access.

**Solutions**:

**Chrome/Edge**:
1. Click the 🔒 or 🔐 icon in the address bar
2. Find "Microphone" in the permissions list
3. Change to "Allow"
4. Refresh the page

**Firefox**:
1. Click the 🔒 or ⓘ icon in the address bar
2. Click on "Permissions" or the arrow next to blocked items
3. Find "Use the Microphone" and select "Allow"
4. Refresh the page

**Safari**:
1. Go to Safari → Settings/Preferences → Websites
2. Click "Microphone" in the left sidebar
3. Find your website and select "Allow"
4. Refresh the page

### 3. "No microphone found"

**Cause**: No microphone device detected.

**Solutions**:
- ✅ Connect a microphone or headset
- ✅ Check if microphone is enabled in system settings
- ✅ Make sure microphone drivers are installed

**Windows**:
- Right-click volume icon → Sounds → Recording tab
- Make sure microphone is enabled and set as default

**Mac**:
- System Preferences → Sound → Input tab
- Make sure microphone is selected and volume is up

**Linux**:
```bash
# Check available audio devices
arecord -l

# Test microphone
arecord -d 5 test.wav
```

### 4. "Microphone is already in use by another application"

**Cause**: Another app is using the microphone.

**Solutions**:
- Close other apps that might use the microphone (Zoom, Skype, Discord, etc.)
- Close other browser tabs that might be using the microphone
- Restart your browser

### 5. Recording button doesn't respond

**Cause**: JavaScript error or browser compatibility issue.

**Solutions**:
1. Open browser console (F12 or Ctrl+Shift+I)
2. Look for errors in the Console tab
3. Try refreshing the page (Ctrl+F5 for hard refresh)
4. Clear browser cache and cookies
5. Try in incognito/private mode

### 6. Recording works but no audio captured

**Cause**: Microphone permission granted but audio level is too low or muted.

**Solutions**:
- Check microphone volume in system settings
- Speak louder and closer to the microphone
- Test microphone with another app to verify it works
- Check if microphone is muted (physical mute button or software)

### 7. "Could not satisfy audio constraints"

**Cause**: Requested audio settings not supported by device.

**Solutions**:
- The app will automatically fall back to supported formats
- Try a different microphone if available
- Update audio drivers

## Browser Compatibility

### Fully Supported:
- ✅ Chrome 60+ (Desktop & Mobile)
- ✅ Firefox 55+ (Desktop & Mobile)
- ✅ Edge 79+ (Chromium-based)
- ✅ Safari 14.1+ (Desktop & iOS)
- ✅ Opera 47+

### Not Supported:
- ❌ Internet Explorer (any version)
- ❌ Old versions of browsers (update to latest)

## Testing the Microphone

### Quick Browser Test:
1. Open browser console (F12)
2. Paste and run:
```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    console.log('✓ Microphone works!');
    stream.getTracks().forEach(track => track.stop());
  })
  .catch(error => console.error('✗ Error:', error));
```

### System Test:

**Windows**:
- Settings → System → Sound → Test your microphone

**Mac**:
- System Preferences → Sound → Input → Watch the input level

**Linux**:
```bash
# Record 5 seconds of audio
arecord -d 5 -f cd test.wav

# Play it back
aplay test.wav
```

## Supported Audio Formats

The webapp now supports multiple recording formats:
- ✅ WEBM (Chrome, Firefox, Edge)
- ✅ OGG (Firefox)
- ✅ MP4/M4A (Safari)
- ✅ WAV (fallback)
- ✅ MP3 (uploaded files)
- ✅ FLAC (uploaded files)

The app automatically selects the best format for your browser.

## Debug Mode

To see detailed logs:
1. Open browser console (F12)
2. Go to the "Voice Translation" tab
3. Click "Start Recording"
4. Watch console for messages:
   - "Requesting microphone access..."
   - "Microphone access granted"
   - "Recording started"
   - "Audio chunk recorded: X bytes"
   - "Recording stopped"

## Still Having Issues?

If none of the above solutions work:

1. **Try a different browser** - Test in Chrome if using Firefox, or vice versa
2. **Restart your computer** - Sometimes audio drivers need a fresh start
3. **Check firewall/antivirus** - Some security software blocks microphone access
4. **Test on a different device** - To rule out hardware issues
5. **Use file upload instead** - Record audio with another app and upload the file

## Recording Tips for Best Results

1. **Speak clearly** and at a normal pace
2. **Reduce background noise** - Find a quiet environment
3. **Position microphone** 6-12 inches from your mouth
4. **Check audio level** before recording
5. **Keep recording under 1 minute** for best results
6. **Test with short phrases** first (like "hello world")

## API Requirements

For the translation to work, you also need:
- ✅ Valid Google Cloud API key in `.env` file
- ✅ Google Cloud Speech-to-Text API enabled
- ✅ Google Cloud Translation API enabled
- ✅ Google Cloud Text-to-Speech API enabled

Check `.env` file:
```bash
GOOGLE_API_KEY=your_api_key_here
```

## Example Usage Flow

1. **Select languages**: Choose source and target language
2. **Go to Voice Translation tab**
3. **Click "Start Recording"** → Browser asks for permission → Click "Allow"
4. **Red indicator appears** → Speak your message
5. **Click "Stop Recording"** → See "Recording saved!" message
6. **Click "Translate Audio"** → Wait for processing
7. **View results** → See transcription and translation with audio

## Console Error Reference

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| `NotAllowedError` | Permission denied | Allow microphone in browser settings |
| `NotFoundError` | No microphone | Connect microphone or check system settings |
| `NotReadableError` | Microphone in use | Close other apps using microphone |
| `OverconstrainedError` | Audio constraints not met | App will use fallback settings |
| `TypeError` | API not supported | Use HTTPS or localhost |

## Performance Notes

- Recording is done locally in the browser (no streaming to server)
- Audio is only sent to server when you click "Translate Audio"
- Typical file size: 50-200 KB per 10 seconds of recording
- Processing time: 5-15 seconds depending on audio length

## Security and Privacy

- Microphone access requires explicit user permission
- Audio is only recorded when you click "Start Recording"
- Recordings are not saved permanently (only during translation)
- Audio is processed via Google Cloud APIs (see Google's privacy policy)

---

**Last Updated**: November 2025
**Version**: 2.0.0
