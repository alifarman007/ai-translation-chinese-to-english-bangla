#!/usr/bin/env python3
"""
Test script for reverse translation (English/Bangla → Chinese)
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.translator import Translator
from src.text_to_speech import TextToSpeech

def test_english_to_chinese():
    """Test English to Chinese translation"""
    print("\n" + "="*60)
    print("TEST 1: English → Chinese Translation")
    print("="*60)

    try:
        translator = Translator()
        tts = TextToSpeech()

        # Test text
        english_text = "hello world"
        print(f"\nOriginal text (English): {english_text}")

        # Translate to Chinese
        result = translator.translate_text(
            text=english_text,
            target_language='zh',
            source_language='en'
        )

        if result['success']:
            chinese_text = result['translated_text']
            print(f"✓ Translation (Chinese): {chinese_text}")

            # Generate audio
            print("\nGenerating Chinese audio...")
            audio_result = tts.synthesize_speech(
                text=chinese_text,
                language_code='zh-CN'
            )

            if audio_result['success']:
                print(f"✓ Audio generated: {audio_result['audio_path']}")
                print(f"  File size: {audio_result['file_size']:.2f} KB")
                return True
            else:
                print(f"✗ Audio generation failed: {audio_result['error']}")
                return False
        else:
            print(f"✗ Translation failed: {result['error']}")
            return False

    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bangla_to_chinese():
    """Test Bangla to Chinese translation"""
    print("\n" + "="*60)
    print("TEST 2: Bangla → Chinese Translation")
    print("="*60)

    try:
        translator = Translator()
        tts = TextToSpeech()

        # Test text (hello world in Bangla)
        bangla_text = "হ্যালো বিশ্ব"
        print(f"\nOriginal text (Bangla): {bangla_text}")

        # Translate to Chinese
        result = translator.translate_text(
            text=bangla_text,
            target_language='zh',
            source_language='bn'
        )

        if result['success']:
            chinese_text = result['translated_text']
            print(f"✓ Translation (Chinese): {chinese_text}")

            # Generate audio
            print("\nGenerating Chinese audio...")
            audio_result = tts.synthesize_speech(
                text=chinese_text,
                language_code='zh-CN'
            )

            if audio_result['success']:
                print(f"✓ Audio generated: {audio_result['audio_path']}")
                print(f"  File size: {audio_result['file_size']:.2f} KB")
                return True
            else:
                print(f"✗ Audio generation failed: {audio_result['error']}")
                return False
        else:
            print(f"✗ Translation failed: {result['error']}")
            return False

    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("REVERSE TRANSLATION TESTS")
    print("="*60)

    # Run tests
    test1_passed = test_english_to_chinese()
    test2_passed = test_bangla_to_chinese()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"English → Chinese: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Bangla → Chinese: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print("="*60)

    if test1_passed and test2_passed:
        print("\n✓ ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)
