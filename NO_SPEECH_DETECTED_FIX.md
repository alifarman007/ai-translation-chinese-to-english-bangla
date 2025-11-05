# No Speech Detected - Troubleshooting Guide

## Problem
Recording is created (10.67 KB), but Google Speech-to-Text API returns "No speech detected in audio file".

## What This Means

The audio file is being recorded and uploaded successfully, but Google's AI cannot detect any recognizable speech patterns in it. This usually means:

1. **Audio is too quiet** - Microphone volume too low
2. **Audio is silence/noise** - Only background noise, no voice
3. **Wrong language selected** - Expecting English but got Chinese, etc.
4. **Audio quality issues** - WEBM encoding might have problems
5. **Speaking too fast/unclear** - Google couldn't understand

## Immediate Solutions

### Solution 1: Use the Diagnostic Tool (Recommended)

1. **Open diagnostic page**:
   ```
   http://localhost:8000/diagnostic.html
   ```

2. **In Section 2 (Recording Test)**:
   - Click "Start Recording"
   - **Speak LOUDLY and CLEARLY**: "Hello, this is a test"
   - Count to 3 slowly
   - Click "Stop Recording"
   - Click "Play Recording" - **Can you hear yourself clearly?**

3. **If you can hear yourself**:
   - Continue to Section 4 (API Test)
   - Select correct language
   - Click "Test Translation API"
   - Check the error details

4. **If you CANNOT hear yourself**:
   - Microphone volume is too low
   - See "Fix Microphone Volume" below

### Solution 2: Check Microphone Volume

**Windows**:
```
1. Right-click volume icon → Sounds
2. Recording tab
3. Select your microphone → Properties
4. Levels tab
5. Set Microphone to 80-100%
6. Set Microphone Boost to +10dB or +20dB
7. Click OK
8. Try recording again
```

**Mac**:
```
1. System Preferences → Sound
2. Input tab
3. Select your microphone
4. Drag Input Volume slider to the right
5. Speak - the level meter should move
6. Try recording again
```

**Linux**:
```bash
# Check microphone
arecord -l

# Set volume to 100%
amixer set Capture 100%

# Test recording
arecord -d 5 test.wav
aplay test.wav
```

### Solution 3: Speak Louder and Closer

When recording:
- **Position**: 6-12 inches from microphone
- **Volume**: Speak **30% louder** than normal
- **Pace**: Speak **slowly** and **clearly**
- **Length**: Say at least 3-5 words (not just "hello")
- **Example**: "Hello world, this is a test message"

### Solution 4: Try Different Browser

Some browsers have better microphone handling:

**Best → Worst**:
1. ✅ **Google Chrome** (best WEBM support)
2. ✅ **Firefox** (good OGG support)
3. ✅ **Edge** (Chromium-based)
4. ⚠️ Safari (uses MP4, sometimes issues)

### Solution 5: Upload File Instead

If recording doesn't work, record with another app:

**Windows**:
```
1. Open "Voice Recorder" app
2. Record your message
3. Save as MP3 or WAV
4. Go to webapp Voice Translation tab
5. Click "Choose Audio File"
6. Select your file
7. Translate
```

**Mac**:
```
1. Open QuickTime Player
2. File → New Audio Recording
3. Record your message
4. Export as MP3
5. Upload to webapp
```

**Phone**:
```
1. Use phone's voice recorder
2. Save as MP3/WAV
3. Transfer to computer
4. Upload to webapp
```

### Solution 6: Test with Pre-recorded Audio

Download a test file to verify the system works:

```bash
# Download a test audio file (you'll need to create one)
# Or use text-to-speech to create a test file

# Then upload it through the webapp
```

## Debugging Steps

### Step 1: Check Server Logs

Look at the terminal where you ran `python main.py`. You should see:

```
[STT] Reading audio file: uploads/20251105_155310_upload.webm
[STT] Audio format detected: webm (WEBM_OPUS)
[STT] Sample rate will be auto-detected by Google API
[STT] Sending to Google Speech-to-Text API (Language: en)...
[STT] Audio size: 10926 bytes
[STT] Response received: XX characters
[STT] Full response: {...}
```

**Look for**:
- `Audio size: X bytes` - Should be > 5000 bytes
- `Full response: {...}` - Shows what Google returned
- Any error messages

### Step 2: Check Browser Console

Press F12, go to Console tab. Look for:

```
Uploading audio file: recording.webm 10926 bytes
Source language: en
Target language: zh
Response status: 500 Internal Server Error
```

**Check**:
- File size should be > 5KB
- Source language should match what you spoke
- Look for any red error messages

### Step 3: Test Audio Playback

In the diagnostic tool:
1. Record something
2. Click "Play Recording"
3. Listen carefully

**What you should hear**:
- ✅ Your voice clearly
- ❌ Silence
- ❌ Just static/noise
- ❌ Very faint voice

If you hear silence or faint voice → Microphone volume too low

### Step 4: Try Different Audio Format

In your browser console (F12), run:

```javascript
// Check supported formats
const formats = [
    'audio/webm',
    'audio/webm;codecs=opus',
    'audio/ogg;codecs=opus',
    'audio/mp4'
];

formats.forEach(f => {
    console.log(f, MediaRecorder.isTypeSupported(f));
});
```

Try using a different browser if current one has limited support.

## Advanced Solutions

### Option 1: Use Enhanced Audio Settings

Edit `static/index.html` and find the `getUserMedia` call. Update it to:

```javascript
const stream = await navigator.mediaDevices.getUserMedia({
    audio: {
        echoCancellation: true,
        noiseSuppression: false,  // Try disabling
        autoGainControl: true,    // Auto boost volume
        sampleRate: 48000,
        channelCount: 1,
        volume: 1.0
    }
});
```

### Option 2: Add Audio Visualization

See if audio is being captured by adding visualization. In the diagnostic tool, you can see the recording level in real-time.

### Option 3: Use Alternative Speech-to-Text

If Google consistently fails, you could:
1. Use text translation instead (type the text)
2. Try a different STT service
3. Use a different audio format (WAV instead of WEBM)

## Common Patterns

### Pattern 1: Works in Diagnostic, Fails in Main App
**Cause**: Different recording settings
**Fix**: Make sure both use same settings

### Pattern 2: Always "No Speech Detected"
**Cause**: Microphone volume too low
**Fix**: Increase microphone boost to +20dB

### Pattern 3: Works with Uploaded Files, Fails with Recording
**Cause**: Recording settings or format issue
**Fix**: Record with another app, save as WAV, upload

### Pattern 4: Works in Chrome, Fails in Firefox
**Cause**: Different audio codecs
**Fix**: Use Chrome for best compatibility

### Pattern 5: Random Success/Failure
**Cause**: Background noise or speaking too quietly
**Fix**: Use quiet environment, speak louder

## Quick Test Checklist

Before requesting help, verify:

- [ ] Microphone works in other apps (Zoom, Discord, etc.)
- [ ] Microphone volume is at 80-100% in system settings
- [ ] Microphone boost is enabled (+10dB or +20dB)
- [ ] You can hear yourself in diagnostic tool playback
- [ ] Speaking loudly and clearly during recording
- [ ] Recording for at least 3 seconds (not instant)
- [ ] Selected correct source language
- [ ] Using latest Chrome or Firefox
- [ ] Server is running (check http://localhost:8000)
- [ ] API key is configured in .env file
- [ ] Text translation works (proves API key is valid)

## Testing Script

Run this test to isolate the issue:

```bash
# Test 1: Text translation (should work)
curl -X POST http://localhost:8000/translate-text \
  -H "Content-Type: application/json" \
  -d '{"text":"hello","source_language":"en","target_languages":["zh"],"generate_audio":true}'

# If above works → API key is good
# If above fails → API key problem

# Test 2: Record in diagnostic tool
# Open: http://localhost:8000/diagnostic.html
# Record → Play → Listen
# If you can hear yourself → Recording works
# If silence → Microphone issue

# Test 3: Upload a known-good file
# Use an existing MP3/WAV file with clear speech
# If works → Recording format issue
# If fails → API or format issue
```

## Expected vs Actual

### Expected Behavior:
```
[STT] Response received: 250 characters
[STT] ✓ Transcription successful
Transcription: "hello world"
Confidence: 95.2%
```

### Current Behavior:
```
[STT] Response received: XX characters
[STT] ✗ No results in API response
[STT] Full response: {}
No speech detected
```

This means Google is returning an empty result, indicating it found no speech in the audio.

## Next Steps

1. **Try diagnostic tool** with loud, clear speech
2. **Check microphone volume** - set to maximum
3. **Enable microphone boost** - +20dB
4. **Speak louder** - 2x normal volume
5. **Try different browser** - Chrome is best
6. **Upload file instead** - if recording doesn't work

## Need More Help?

If still not working after trying above:
1. Run diagnostic tool
2. Copy the Console Log (Section 5)
3. Check server terminal output
4. Try uploading a pre-recorded file
5. Report exact error from diagnostic tool

The most common fix is: **Increase microphone volume and speak much louder!**

---

**Updated**: November 2025 with enhanced logging
