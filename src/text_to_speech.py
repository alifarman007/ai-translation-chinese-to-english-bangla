import os
import requests
from dotenv import load_dotenv
import base64
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class TextToSpeech:
    def __init__(self):
        """Initialize Text-to-Speech with API key"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        self.base_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        
        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)
        
        print(f"[TTS] ✓ API Key loaded successfully")
        
    def synthesize_speech(self, text, language_code='en-US', voice_name=None, output_path=None):
        """
        Convert text to speech
        
        Args:
            text (str): Text to convert to speech
            language_code (str): Language code (e.g., 'en-US', 'bn-IN')
            voice_name (str): Specific voice name (optional)
            output_path (str): Output file path (optional, auto-generated if not provided)
            
        Returns:
            dict: Result with audio file path
        """
        try:
            print(f"[TTS] Synthesizing speech for {language_code}...")
            print(f"[TTS] Text: {text[:50]}..." if len(text) > 50 else f"[TTS] Text: {text}")
            
            # Auto-generate output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                lang_short = language_code.split('-')[0]
                output_path = f"outputs/audio_{lang_short}_{timestamp}.mp3"
            
            # Configure voice settings
            voice_config = {
                "languageCode": language_code
            }
            
            # Add specific voice if provided
            if voice_name:
                voice_config["name"] = voice_name
            else:
                # Use default voices
                default_voices = {
                    'en-US': 'en-US-Neural2-C',  # Female voice
                    'bn-IN': 'bn-IN-Standard-A',  # Bangla female voice
                }
                if language_code in default_voices:
                    voice_config["name"] = default_voices[language_code]
            
            # Prepare request payload
            request_data = {
                "input": {
                    "text": text
                },
                "voice": voice_config,
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "pitch": 0.0,
                    "speakingRate": 1.0
                }
            }
            
            # Make API request
            url = f"{self.base_url}?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(request_data),
                timeout=60
            )
            
            # Check response
            if response.status_code != 200:
                error_detail = response.json() if response.text else 'Unknown error'
                return {
                    'success': False,
                    'audio_path': '',
                    'error': f'TTS API Error ({response.status_code}): {error_detail}'
                }
            
            # Parse response
            result = response.json()
            
            if 'audioContent' not in result:
                return {
                    'success': False,
                    'audio_path': '',
                    'error': 'No audio content in response'
                }
            
            # Decode base64 audio content
            audio_content = base64.b64decode(result['audioContent'])
            
            # Save audio file
            with open(output_path, 'wb') as audio_file:
                audio_file.write(audio_content)
            
            file_size = len(audio_content) / 1024  # KB
            
            print(f"[TTS] ✓ Speech synthesis successful")
            print(f"[TTS] Saved to: {output_path} ({file_size:.2f} KB)")
            
            return {
                'success': True,
                'audio_path': output_path,
                'file_size': file_size,
                'language': language_code
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'audio_path': '',
                'error': 'TTS request timeout'
            }
            
        except Exception as e:
            return {
                'success': False,
                'audio_path': '',
                'error': f'TTS error: {str(e)}'
            }
    
    def synthesize_multiple(self, translations_dict):
        """
        Generate speech for multiple translations
        
        Args:
            translations_dict (dict): Dictionary with language translations
                Example: {
                    'english': {'text': 'Hello world', 'language_code': 'en'},
                    'bangla': {'text': 'হ্যালো বিশ্ব', 'language_code': 'bn'}
                }
            
        Returns:
            dict: Audio paths for all languages
        """
        print(f"\n[TTS] Generating speech for {len(translations_dict)} languages...")
        
        results = {}
        all_success = True
        
        language_map = {
            'en': 'en-US',
            'bn': 'bn-IN'
        }
        
        for lang_name, translation in translations_dict.items():
            if not translation.get('success', True):
                continue
                
            text = translation['text']
            lang_code = translation['language_code']
            
            # Map to TTS language code
            tts_lang_code = language_map.get(lang_code, lang_code)
            
            print(f"\n[TTS] → Generating {lang_name.capitalize()} audio...")
            
            result = self.synthesize_speech(text, tts_lang_code)
            
            if result['success']:
                results[lang_name] = {
                    'audio_path': result['audio_path'],
                    'file_size': result['file_size'],
                    'success': True
                }
            else:
                results[lang_name] = {
                    'audio_path': '',
                    'success': False,
                    'error': result['error']
                }
                all_success = False
        
        return {
            'success': all_success,
            'audio_files': results
        }


# Test function
def test_text_to_speech():
    """Test the Text-to-Speech functionality"""
    print("\n" + "="*60)
    print("Testing Text-to-Speech Module (REST API)")
    print("="*60)
    
    try:
        tts = TextToSpeech()
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        return
    
    # Test texts
    print("\nChoose test option:")
    print("1. Default text (Hello World)")
    print("2. Custom text")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '2':
        english_text = input("Enter English text: ").strip()
        bangla_text = input("Enter Bangla text: ").strip()
    else:
        english_text = "Hello world, this is a test of text to speech."
        bangla_text = "হ্যালো বিশ্ব, এটি একটি পরীক্ষা।"
    
    # Prepare translations dictionary
    translations = {
        'english': {
            'text': english_text,
            'language_code': 'en',
            'success': True
        },
        'bangla': {
            'text': bangla_text,
            'language_code': 'bn',
            'success': True
        }
    }
    
    # Generate speech
    result = tts.synthesize_multiple(translations)
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    
    if result['success']:
        print(f"\n✓ All audio files generated successfully!\n")
        
        for lang_name, audio_info in result['audio_files'].items():
            if audio_info['success']:
                print(f"{lang_name.capitalize()}:")
                print(f"  ✓ File: {audio_info['audio_path']}")
                print(f"  Size: {audio_info['file_size']:.2f} KB")
            else:
                print(f"{lang_name.capitalize()}: ✗ Failed")
                print(f"  Error: {audio_info.get('error', 'Unknown')}")
        
        print(f"\n💡 Play the audio files to hear the results!")
        print(f"   Files saved in: outputs/")
        
    else:
        print(f"\n✗ Some audio generation failed!")
        
        for lang_name, audio_info in result['audio_files'].items():
            if audio_info['success']:
                print(f"\n{lang_name.capitalize()}: ✓ Success")
                print(f"  File: {audio_info['audio_path']}")
            else:
                print(f"\n{lang_name.capitalize()}: ✗ Failed")
                print(f"  Error: {audio_info.get('error', 'Unknown')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_text_to_speech()