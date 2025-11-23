#!/usr/bin/env python3
"""
Test script for the new /speech-to-text API endpoint
"""

import requests
import sys
import os

def test_speech_to_text_endpoint(audio_file_path):
    """
    Test the /speech-to-text endpoint

    Args:
        audio_file_path (str): Path to audio file
    """

    # API endpoint
    url = "http://localhost:8000/speech-to-text"

    # Check if file exists
    if not os.path.exists(audio_file_path):
        print(f"Error: File not found: {audio_file_path}")
        return

    # Prepare the file
    with open(audio_file_path, 'rb') as audio_file:
        files = {
            'file': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg')
        }

        print(f"\nTesting /speech-to-text endpoint")
        print(f"File: {audio_file_path}")
        print(f"Language: Auto-detection (Chinese, English, Bangla)")
        print(f"Sending request to: {url}")
        print("-" * 60)

        try:
            # Make the request
            response = requests.post(url, files=files)

            # Check response
            if response.status_code == 200:
                result = response.json()
                print("\n✓ SUCCESS!")
                print(f"Text: {result.get('text', 'N/A')}")
                print(f"Confidence: {result.get('confidence', 0):.2%}")
                print(f"Language: {result.get('language', 'N/A')}")
                print(f"Processing Time: {result.get('processing_time', 0):.2f}s")
                print(f"Timestamp: {result.get('timestamp', 'N/A')}")
            else:
                print(f"\n✗ FAILED (Status Code: {response.status_code})")
                print(f"Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n✗ ERROR: Could not connect to server")
            print("Make sure the server is running at http://localhost:8000")
        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python test_speech_to_text_api.py <audio_file_path>")
        print("\nExample:")
        print("  python test_speech_to_text_api.py uploads/test.mp3")
        print("  python test_speech_to_text_api.py uploads/english.wav")
        print("\nLanguage auto-detection:")
        print("  The API automatically detects language among:")
        print("  - Chinese (Mandarin)")
        print("  - English")
        print("  - Bangla")
        sys.exit(1)

    audio_file = sys.argv[1]

    test_speech_to_text_endpoint(audio_file)
