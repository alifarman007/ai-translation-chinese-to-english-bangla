# Recording Translation Debug Guide

## Problem
Recording works, but translation fails with "❌ Translation failed" error.

## What Was Fixed

### 1. **Better Error Messages** ✅
Updated frontend to show detailed error information instead of just "Translation failed"

### 2. **Sample Rate Issue** ✅
Fixed the sample rate configuration for recorded audio:
- **Before**: Hardcoded 16000 Hz for all formats (incorrect for browser recordings)
- **After**: Auto-detection for WEBM/OGG/MP3 formats (browser typically records at 48000 Hz)

### 3. **Diagnostic Tool** ✅
Created a comprehensive diagnostic page at `/diagnostic.html` to test each component

## How to Debug the Issue

### Step 1: Use the Diagnostic Tool

1. **Start the server**:
   ```bash
   python main.py
   ```

2. **Open the diagnostic page**:
   ```
   http://localhost:8000/diagnostic.html
   ```

3. **Follow the diagnostic steps**:

#### Section 1: Browser Compatibility Check
- Should show all green checkmarks
- Shows which audio formats your browser supports
- **Expected**: WEBM or OGG should be supported

#### Section 2: Recording Test
1. Click "Start Recording"
2. Allow microphone permission
3. Speak clearly: "hello" or "hello world"
4. Click "Stop Recording"
5. Click "Play Recording" to verify audio was captured
6. **Expected**: You should hear your voice clearly

#### Section 3: Server Connection Check
1. Click "Check Server"
2. **Expected**: "✅ Server is running" with JSON health response

#### Section 4: API Test
1. Select language (English if you spoke English)
2. Click "Test Translation API"
3. **Watch the result carefully**:
   - ✅ **Success**: Shows transcription and translation
   - ❌ **Failure**: Shows detailed error message

#### Section 5: Console Log
- Shows all operations step-by-step
- Look for specific error messages
- Copy and share this log if you need help

### Step 2: Check the Browser Console

1. Press **F12** to open Developer Tools
2. Go to **Console** tab
3. Try recording and translating again
4. Look for error messages in red

Common errors and solutions:

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `GOOGLE_API_KEY not found` | API key not configured | Add key to `.env` file |
| `Invalid API key` | Wrong API key | Check your Google Cloud API key |
| `API not enabled` | Google APIs not enabled | Enable Speech-to-Text, Translation, and Text-to-Speech APIs in Google Cloud Console |
| `Invalid encoding` | Audio format not supported | Browser should use WEBM/OGG (check diagnostic tool) |
| `Sample rate mismatch` | Fixed in this update | Make sure you're using the latest code |
| `No speech detected` | Spoke too quietly | Speak louder, closer to microphone |
| `Language not supported` | Wrong language code | Use 'en' for English, 'zh-CN' for Chinese, 'bn' for Bangla |

### Step 3: Test Text Translation First

To verify your API key works:

1. Go to main page: `http://localhost:8000`
2. Click **"Text Translation"** tab
3. Type: "hello" or "你好"
4. Select languages
5. Click "Translate Text"

**If text translation works** = API key is correct
**If text translation fails** = API key issue

### Step 4: Check Backend Logs

In the terminal where you ran `python main.py`, you'll see detailed logs:

```
[STT] Reading audio file: uploads/20251105_120000_upload.webm
[STT] Audio format detected: webm (WEBM_OPUS)
[STT] Sample rate will be auto-detected by Google API
[STT] Sending to Google Speech-to-Text API (Language: en)...
[STT] ✓ Transcription successful
[Translator] Translating English text to 1 languages...
...
```

Look for error messages or where the process stops.

## Common Issues and Solutions

### Issue 1: "Translation failed" with no details

**Cause**: Old frontend code
**Solution**: Refresh page with Ctrl+F5 (hard refresh)

### Issue 2: API Key Error

**Cause**: `.env` file not configured

**Solution**:
1. Create/edit `.env` file in project root:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```
2. Get API key from: https://console.cloud.google.com/apis/credentials
3. Restart server

### Issue 3: "No speech detected" in API response

**Cause**: Audio too quiet or wrong language selected

**Solutions**:
- Speak louder and clearer
- Verify you selected the correct source language
- Test with diagnostic tool to hear your recording
- Try saying a longer phrase

### Issue 4: WEBM format not supported

**Cause**: Using old browser

**Solutions**:
- Update browser to latest version
- Use Chrome or Firefox (best support)
- Safari will record in MP4 (also supported)

### Issue 5: Sample rate error

**Cause**: Fixed in this update

**Solution**: Make sure you have the latest code with auto-detection

## Verification Checklist

Before reporting an issue, verify:

- [ ] Server is running (check with diagnostic tool)
- [ ] Browser supports recording (check section 1 of diagnostic)
- [ ] Can record and play back audio (check section 2)
- [ ] Microphone permission granted
- [ ] API key is in `.env` file
- [ ] Text translation works (proves API key is valid)
- [ ] Selected correct source language
- [ ] Spoke clearly during recording
- [ ] Refreshed page after code updates (Ctrl+F5)

## Testing Steps

### Test 1: Simple English → Chinese
1. Open http://localhost:8000
2. Select: Source = English, Target = Chinese
3. Go to Voice Translation tab
4. Record: "hello"
5. Translate
6. **Expected**:
   - Transcription: "hello" or "Hello"
   - Translation: "你好" or "您好"
   - Chinese audio plays

### Test 2: Using Diagnostic Tool
1. Open http://localhost:8000/diagnostic.html
2. Complete all 5 sections
3. Section 4 should show successful translation
4. Console log should show no errors

## What the Error Message Tells You

With the updated frontend, you'll now see detailed errors like:

### Error Example 1: API Key Issue
```
Translation failed: Translation pipeline not initialized
```
**Solution**: Server couldn't load pipeline, check if API key is in `.env`

### Error Example 2: Google API Error
```
Translation failed: Speech-to-Text failed: STT API Error (400): Invalid audio encoding
```
**Solution**: Audio format issue (fixed with sample rate update)

### Error Example 3: Permission Error
```
Translation failed: API not enabled
```
**Solution**: Enable the required APIs in Google Cloud Console

## Files Changed in This Update

1. **static/index.html**
   - Added detailed error logging
   - Shows complete error messages from backend
   - Console logging for debugging

2. **static/diagnostic.html** (NEW)
   - Complete diagnostic tool
   - Tests each component separately
   - Shows exactly where the problem is

3. **src/speech_to_text.py**
   - Fixed sample rate configuration
   - Auto-detection for WEBM/OGG/MP3
   - Better format handling

## Next Steps

1. **Try the diagnostic tool** first: http://localhost:8000/diagnostic.html
2. **Record in diagnostic tool** and test API
3. **Check the error message** in Section 4
4. **Share the Console Log** (Section 5) if you need help

The new error messages will tell you exactly what's wrong!

## Expected Output Example

When everything works correctly, the diagnostic tool will show:

```
✅ Browser Check: All supported
✅ Recording: 102400 bytes captured
✅ Server: Running and healthy
✅ API Test:
   Transcription: "hello"
   Confidence: 95.2%
   Translation: "你好"
```

---

**Important**: The sample rate fix should resolve most recording translation issues. The diagnostic tool will help identify any remaining problems.
