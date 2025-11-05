#!/usr/bin/env python3
"""
Test script to verify the file upload fix for speech-to-text
"""

import os
import sys
from src.speech_to_text import SpeechToText

def test_file_upload_fix():
    """Test the enhanced speech-to-text with audio optimization"""
    
    print("="*60)
    print("Testing File Upload Fix for Speech-to-Text")
    print("="*60)
    
    try:
        # Initialize STT
        stt = SpeechToText()
        print("\n✓ Speech-to-Text module initialized")
        
        # Find a test file
        test_files = [
            'uploads/chinese_test.mp3',
            'uploads/20251105_161812_upload.mp3',
            'uploads/20251105_152142_upload.mp3'
        ]
        
        test_file = None
        for f in test_files:
            if os.path.exists(f):
                test_file = f
                break
        
        if not test_file:
            print("\n❌ No test files found")
            print("Please upload an audio file through the web interface first")
            return False
        
        print(f"\n📁 Testing with: {test_file}")
        print(f"📏 File size: {os.path.getsize(test_file)} bytes")
        
        # Test transcription with the enhanced method
        print(f"\n🔄 Testing transcription...")
        
        # Test with different language codes
        languages_to_test = ['zh-CN', 'en', 'auto']
        
        for lang in languages_to_test:
            if lang == 'auto':
                # Skip auto for now
                continue
                
            print(f"\n--- Testing language: {lang} ---")
            
            result = stt.transcribe_audio(test_file, lang)
            
            if result['success']:
                print(f"✅ SUCCESS for {lang}!")
                print(f"   Transcription: {result['transcription']}")
                print(f"   Confidence: {result['confidence']:.2%}")
                return True
            else:
                print(f"❌ Failed for {lang}: {result['error']}")
        
        print(f"\n❌ All language tests failed")
        return False
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("File Upload Translation Fix - Test Suite")
    print("This tests the enhanced audio processing for uploaded files")
    
    success = test_file_upload_fix()
    
    print("\n" + "="*60)
    if success:
        print("🎉 TEST PASSED! File upload translation should now work!")
        print("\nThe fix includes:")
        print("✓ Audio optimization (convert to FLAC 16kHz mono)")
        print("✓ Volume boosting for better speech detection")
        print("✓ Proper sample rate configuration")
        print("✓ Temporary file cleanup")
        print("\nYou can now upload various audio formats and they should work!")
        
    else:
        print("❌ TEST FAILED")
        print("\nPossible issues:")
        print("- API key not configured correctly")
        print("- No suitable test files available")
        print("- Network connectivity issues")
        print("- Audio file doesn't contain clear speech")
        
    print("="*60)

if __name__ == "__main__":
    main()