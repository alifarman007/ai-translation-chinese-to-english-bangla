import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class Translator:
    def __init__(self):
        """Initialize Translator with API key"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
        print(f"[Translator] ✓ API Key loaded successfully")
        
    def translate_text(self, text, target_language, source_language='zh-CN'):
        """
        Translate text to target language
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code (e.g., 'en', 'bn')
            source_language (str): Source language code (default: zh-CN)
            
        Returns:
            dict: Translation result
        """
        try:
            # Prepare request parameters
            params = {
                'key': self.api_key,
                'q': text,
                'target': target_language,
                'source': source_language,
                'format': 'text'
            }
            
            print(f"[Translator] Translating to {target_language}...")
            
            # Make API request
            response = requests.post(
                self.base_url,
                params=params,
                timeout=30
            )
            
            # Check response
            if response.status_code != 200:
                error_detail = response.json() if response.text else 'Unknown error'
                return {
                    'success': False,
                    'translated_text': '',
                    'error': f'Translation API Error ({response.status_code}): {error_detail}'
                }
            
            # Parse response
            result = response.json()
            
            if 'data' not in result or 'translations' not in result['data']:
                return {
                    'success': False,
                    'translated_text': '',
                    'error': 'Invalid response from Translation API'
                }
            
            translated_text = result['data']['translations'][0]['translatedText']
            detected_language = result['data']['translations'][0].get('detectedSourceLanguage', source_language)
            
            print(f"[Translator] ✓ Translation successful")
            print(f"[Translator] Result: {translated_text}")
            
            return {
                'success': True,
                'translated_text': translated_text,
                'source_language': detected_language,
                'target_language': target_language
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'translated_text': '',
                'error': 'Translation request timeout'
            }
            
        except Exception as e:
            return {
                'success': False,
                'translated_text': '',
                'error': f'Translation error: {str(e)}'
            }
    
    def translate_to_multiple(self, text, target_languages=['en', 'bn'], source_language='zh-CN'):
        """
        Translate text to multiple languages
        
        Args:
            text (str): Text to translate
            target_languages (list): List of target language codes
            source_language (str): Source language code
            
        Returns:
            dict: Translations for all target languages
        """
        print(f"\n[Translator] Translating Chinese text to {len(target_languages)} languages...")
        print(f"[Translator] Source text: {text}")
        
        results = {}
        all_success = True
        
        for lang in target_languages:
            lang_name = {
                'en': 'English',
                'bn': 'Bangla'
            }.get(lang, lang)
            
            print(f"\n[Translator] → Translating to {lang_name} ({lang})...")
            
            result = self.translate_text(text, lang, source_language)
            
            if result['success']:
                results[lang_name.lower()] = {
                    'text': result['translated_text'],
                    'language_code': lang,
                    'success': True
                }
            else:
                results[lang_name.lower()] = {
                    'text': '',
                    'language_code': lang,
                    'success': False,
                    'error': result['error']
                }
                all_success = False
        
        return {
            'success': all_success,
            'translations': results,
            'source_text': text,
            'source_language': source_language
        }


# Test function
def test_translator():
    """Test the Translator functionality"""
    print("\n" + "="*60)
    print("Testing Translation Module (REST API)")
    print("="*60)
    
    try:
        translator = Translator()
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        return
    
    # Test with Chinese text
    test_text = input("\nEnter Chinese text to translate (or press Enter for default): ").strip()
    
    if not test_text:
        test_text = "你好世界，这是一个测试"
        print(f"Using default text: {test_text}")
    
    # Translate to both English and Bangla
    result = translator.translate_to_multiple(test_text, target_languages=['en', 'bn'])
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    
    if result['success']:
        print(f"\n✓ All translations successful!")
        print(f"\nOriginal (Chinese): {result['source_text']}")
        
        for lang_name, translation in result['translations'].items():
            if translation['success']:
                print(f"\n{lang_name.capitalize()}:")
                print(f"  Text: {translation['text']}")
                print(f"  Code: {translation['language_code']}")
            else:
                print(f"\n{lang_name.capitalize()}: ✗ Failed")
                print(f"  Error: {translation.get('error', 'Unknown error')}")
    else:
        print(f"\n✗ Some translations failed!")
        print(f"\nOriginal (Chinese): {result['source_text']}")
        
        for lang_name, translation in result['translations'].items():
            if translation['success']:
                print(f"\n{lang_name.capitalize()}: ✓ Success")
                print(f"  Text: {translation['text']}")
            else:
                print(f"\n{lang_name.capitalize()}: ✗ Failed")
                print(f"  Error: {translation.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_translator()