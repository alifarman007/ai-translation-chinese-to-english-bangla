import os
import requests
import base64
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class SpeechToText:
    def __init__(self):
        """Initialize Speech-to-Text with API key"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        self.base_url = "https://speech.googleapis.com/v1/speech:recognize"
        print(f"[STT] ✓ API Key loaded successfully")
        
    def transcribe_audio(self, audio_file_path, language_code='zh-CN'):
        """
        Transcribe audio file to text using REST API

        Args:
            audio_file_path (str): Path to audio file (WAV, MP3, FLAC, WEBM, OGG, MP4, M4A)
            language_code (str): Language code (default: zh-CN for Mandarin)

        Returns:
            dict: Contains transcription and confidence score
        """
        try:
            print(f"[STT] Reading audio file: {audio_file_path}")
            
            # Check if file exists
            if not os.path.exists(audio_file_path):
                return {
                    'success': False,
                    'transcription': '',
                    'confidence': 0.0,
                    'error': f'Audio file not found: {audio_file_path}'
                }
            
            # Read and encode audio file to base64
            with open(audio_file_path, 'rb') as audio_file:
                audio_content = audio_file.read()
                audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            
            # Determine audio encoding from file extension
            file_extension = audio_file_path.lower().split('.')[-1]

            encoding_map = {
                'wav': 'LINEAR16',
                'mp3': 'MP3',
                'flac': 'FLAC',
                'webm': 'WEBM_OPUS',
                'ogg': 'OGG_OPUS',
                'mp4': 'MP3',
                'm4a': 'MP3'
            }

            if file_extension not in encoding_map:
                return {
                    'success': False,
                    'transcription': '',
                    'confidence': 0.0,
                    'error': f'Unsupported audio format: {file_extension}. Supported formats: WAV, MP3, FLAC, WEBM, OGG, MP4, M4A'
                }

            encoding = encoding_map[file_extension]
            print(f"[STT] Audio format detected: {file_extension} ({encoding})")

            # Configure sample rate based on format
            # For WEBM_OPUS, OGG_OPUS, and MP3, Google can auto-detect
            # For LINEAR16 and FLAC, we should specify it
            config = {
                "encoding": encoding,
                "languageCode": language_code,
                "enableAutomaticPunctuation": True
            }

            # Only add sampleRateHertz for formats that need it
            if encoding in ['LINEAR16', 'FLAC']:
                config["sampleRateHertz"] = 16000
                print(f"[STT] Using sample rate: 16000 Hz")
            else:
                print(f"[STT] Sample rate will be auto-detected by Google API")

            # Prepare request payload
            request_data = {
                "config": config,
                "audio": {
                    "content": audio_base64
                }
            }
            
            print(f"[STT] Sending to Google Speech-to-Text API (Language: {language_code})...")
            print(f"[STT] Audio size: {len(audio_content)} bytes")

            # Make API request
            url = f"{self.base_url}?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}

            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(request_data),
                timeout=60
            )

            # Check response status
            if response.status_code != 200:
                error_detail = response.json() if response.text else 'Unknown error'
                print(f"[STT] ✗ API Error: {response.status_code}")
                print(f"[STT] Error details: {error_detail}")
                return {
                    'success': False,
                    'transcription': '',
                    'confidence': 0.0,
                    'error': f'API Error ({response.status_code}): {error_detail}'
                }

            # Parse response
            result = response.json()
            print(f"[STT] Response received: {len(str(result))} characters")

            # Check if results exist
            if 'results' not in result or not result['results']:
                print(f"[STT] ✗ No results in API response")
                print(f"[STT] Full response: {result}")

                # Check if there's an error in the response
                if 'error' in result:
                    error_msg = result['error'].get('message', 'Unknown error')
                    return {
                        'success': False,
                        'transcription': '',
                        'confidence': 0.0,
                        'error': f'Google API Error: {error_msg}'
                    }

                # No speech detected - provide helpful message
                return {
                    'success': False,
                    'transcription': '',
                    'confidence': 0.0,
                    'error': 'No speech detected. Try: 1) Speaking louder and closer to mic, 2) Recording a longer phrase, 3) Using the diagnostic tool to test your recording, 4) Uploading a pre-recorded file instead'
                }
            
            # Extract transcription
            transcript = result['results'][0]['alternatives'][0]['transcript']
            confidence = result['results'][0]['alternatives'][0].get('confidence', 0.0)
            
            print(f"[STT] ✓ Transcription successful (Confidence: {confidence:.2%})")
            print(f"[STT] Text: {transcript}")
            
            return {
                'success': True,
                'transcription': transcript,
                'confidence': confidence,
                'language': language_code
            }
            
        except FileNotFoundError:
            return {
                'success': False,
                'transcription': '',
                'confidence': 0.0,
                'error': f'Audio file not found: {audio_file_path}'
            }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'transcription': '',
                'confidence': 0.0,
                'error': 'Request timeout - audio file might be too large'
            }
            
        except Exception as e:
            return {
                'success': False,
                'transcription': '',
                'confidence': 0.0,
                'error': f'Speech-to-Text error: {str(e)}'
            }


# Test function
def test_speech_to_text():
    """Test the Speech-to-Text functionality"""
    print("\n" + "="*60)
    print("Testing Speech-to-Text Module (REST API)")
    print("="*60)
    
    try:
        stt = SpeechToText()
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("Make sure your .env file contains GOOGLE_API_KEY")
        return
    
    # Test with your audio file
    test_audio = input("\nEnter path to your Chinese audio file: ").strip()
    
    if not test_audio:
        print("✗ No file path provided")
        return
    
    if not os.path.exists(test_audio):
        print(f"✗ File not found: {test_audio}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in uploads/:")
        if os.path.exists('uploads'):
            print(os.listdir('uploads'))
        return
    
    # Show file info
    file_size = os.path.getsize(test_audio)
    print(f"\n[INFO] File size: {file_size / 1024:.2f} KB")
    
    if file_size > 10 * 1024 * 1024:  # 10MB limit
        print("⚠ Warning: File is large, this may take a while...")
    
    result = stt.transcribe_audio(test_audio)
    
    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    
    if result['success']:
        print(f"✓ Success!")
        print(f"Transcription: {result['transcription']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Language: {result['language']}")
    else:
        print(f"✗ Failed!")
        print(f"Error: {result['error']}")
    
    print("="*60)


if __name__ == "__main__":
    test_speech_to_text()