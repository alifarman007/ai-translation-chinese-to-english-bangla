import os
import requests
import base64
from dotenv import load_dotenv
import json
import subprocess
import tempfile
import shutil

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
        
        # Check if ffmpeg is available for audio conversion
        self.ffmpeg_available = self._check_ffmpeg()
        if self.ffmpeg_available:
            print(f"[STT] ✓ FFmpeg available for audio optimization")
        else:
            print(f"[STT] ⚠ FFmpeg not found - will process files directly")
    
    def _check_ffmpeg(self):
        """Check if ffmpeg is installed"""
        try:
            return shutil.which('ffmpeg') is not None
        except:
            return False
    
    def _optimize_audio_for_stt(self, input_path):
        """
        Convert audio to optimal format for Google Speech-to-Text:
        - FLAC format (best compression + quality)
        - 16kHz sample rate (optimal for speech recognition)
        - Mono channel (reduces file size and improves accuracy)
        
        Args:
            input_path (str): Path to original audio file
            
        Returns:
            str: Path to optimized file, or original path if conversion fails
        """
        if not self.ffmpeg_available:
            print(f"[STT] FFmpeg not available - using original file")
            return input_path
            
        try:
            # Create temporary file for optimized audio
            temp_dir = tempfile.gettempdir()
            optimized_path = os.path.join(temp_dir, f"optimized_{os.path.basename(input_path)}.flac")
            
            # FFmpeg command to optimize for speech recognition
            cmd = [
                'ffmpeg',
                '-i', input_path,           # Input file
                '-ac', '1',                 # Convert to mono
                '-ar', '16000',            # 16kHz sample rate
                '-af', 'volume=2.0',       # Boost volume by 2x
                '-compression_level', '8',  # High compression for FLAC
                '-y',                      # Overwrite output
                optimized_path
            ]
            
            print(f"[STT] Optimizing audio: {os.path.basename(input_path)} -> FLAC")
            
            # Run conversion with timeout
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(optimized_path):
                original_size = os.path.getsize(input_path)
                optimized_size = os.path.getsize(optimized_path)
                print(f"[STT] ✓ Audio optimized: {original_size//1024}KB -> {optimized_size//1024}KB")
                return optimized_path
            else:
                print(f"[STT] ⚠ Audio optimization failed: {result.stderr}")
                return input_path
                
        except Exception as e:
            print(f"[STT] ⚠ Audio optimization error: {e}")
            return input_path
        
    def transcribe_audio(self, audio_file_path, language_code='zh-CN'):
        """
        Transcribe audio file to text using REST API

        Args:
            audio_file_path (str): Path to audio file (WAV, MP3, FLAC, WEBM, OGG, MP4, M4A)
            language_code (str): Language code (default: zh-CN for Mandarin)

        Returns:
            dict: Contains transcription and confidence score
        """
        optimized_file_path = None
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
            
            # Optimize audio for better speech recognition (if ffmpeg available)
            optimized_file_path = self._optimize_audio_for_stt(audio_file_path)
            processing_file_path = optimized_file_path
            
            # Read and encode the (optimized) audio file to base64
            with open(processing_file_path, 'rb') as audio_file:
                audio_content = audio_file.read()
                audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            
            # Determine audio encoding from the processing file (may be optimized)
            file_extension = processing_file_path.lower().split('.')[-1]

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

            # Configure sample rate based on format and whether file was optimized
            config = {
                "encoding": encoding,
                "languageCode": language_code,
                "enableAutomaticPunctuation": True
            }

            # If we optimized the file, we know it's 16kHz
            # Otherwise, handle original file formats
            if processing_file_path != audio_file_path:
                # File was optimized to FLAC 16kHz mono
                config["sampleRateHertz"] = 16000
                print(f"[STT] Using optimized audio: FLAC, 16kHz, mono")
            elif encoding in ['LINEAR16', 'FLAC']:
                # Original WAV/FLAC files need explicit sample rate
                config["sampleRateHertz"] = 16000
                print(f"[STT] Using sample rate: 16000 Hz")
            else:
                # For MP3, WEBM, OGG - try to specify 16kHz for better results
                config["sampleRateHertz"] = 16000
                print(f"[STT] Using sample rate: 16000 Hz (optimized for speech recognition)")

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
        
        finally:
            # Clean up optimized temporary file
            if optimized_file_path and optimized_file_path != audio_file_path:
                try:
                    if os.path.exists(optimized_file_path):
                        os.remove(optimized_file_path)
                        print(f"[STT] ✓ Cleaned up temporary file")
                except Exception as e:
                    print(f"[STT] ⚠ Could not clean up temporary file: {e}")


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