import os
import time
from datetime import datetime
from .speech_to_text import SpeechToText
from .translator import Translator
from .text_to_speech import TextToSpeech

class TranslationPipeline:
    def __init__(self):
        """Initialize all components of the translation pipeline"""
        print("\n" + "="*60)
        print("Initializing Translation Pipeline")
        print("="*60)
        
        try:
            self.stt = SpeechToText()
            self.translator = Translator()
            self.tts = TextToSpeech()
            
            print("[Pipeline] ✓ All modules initialized successfully")
            
        except Exception as e:
            print(f"[Pipeline] ✗ Initialization failed: {e}")
            raise
    
    def process_audio(self, audio_file_path, source_language='zh-CN', target_languages=['en', 'bn']):
        """
        Complete translation pipeline: Audio → Text → Translation → Speech
        
        Args:
            audio_file_path (str): Path to Chinese audio file
            source_language (str): Source language code (default: zh-CN for Mandarin)
            target_languages (list): Target language codes (default: ['en', 'bn'])
            
        Returns:
            dict: Complete result with all outputs
        """
        start_time = time.time()
        
        print("\n" + "="*60)
        print("TRANSLATION PIPELINE STARTED")
        print("="*60)
        print(f"Input file: {audio_file_path}")
        print(f"Source language: {source_language}")
        print(f"Target languages: {', '.join(target_languages)}")
        print("="*60)
        
        result = {
            'success': False,
            'input_file': audio_file_path,
            'transcription': {},
            'translations': {},
            'audio_outputs': {},
            'processing_time': 0,
            'timestamp': datetime.now().isoformat(),
            'errors': []
        }
        
        # Step 1: Speech-to-Text
        print("\n[STEP 1/3] Speech-to-Text Processing...")
        print("-" * 60)
        
        stt_result = self.stt.transcribe_audio(audio_file_path, source_language)
        
        if not stt_result['success']:
            error_msg = f"Speech-to-Text failed: {stt_result['error']}"
            print(f"✗ {error_msg}")
            result['errors'].append(error_msg)
            result['processing_time'] = time.time() - start_time
            return result
        
        result['transcription'] = {
            'text': stt_result['transcription'],
            'confidence': stt_result['confidence'],
            'language': stt_result['language']
        }
        
        print(f"✓ Transcription successful")
        print(f"  Text: {stt_result['transcription']}")
        print(f"  Confidence: {stt_result['confidence']:.2%}")
        
        # Step 2: Translation
        print("\n[STEP 2/3] Translation Processing...")
        print("-" * 60)
        
        translation_result = self.translator.translate_to_multiple(
            stt_result['transcription'],
            target_languages=target_languages,
            source_language=source_language
        )
        
        if not translation_result['success']:
            error_msg = "Translation failed for some languages"
            print(f"⚠ {error_msg}")
            result['errors'].append(error_msg)
        
        result['translations'] = translation_result['translations']
        
        # Display translations
        print(f"\n✓ Translation completed")
        for lang_name, translation in translation_result['translations'].items():
            if translation['success']:
                print(f"  {lang_name.capitalize()}: {translation['text']}")
            else:
                print(f"  {lang_name.capitalize()}: ✗ Failed")
        
        # Step 3: Text-to-Speech
        print("\n[STEP 3/3] Text-to-Speech Processing...")
        print("-" * 60)
        
        tts_result = self.tts.synthesize_multiple(translation_result['translations'])
        
        if not tts_result['success']:
            error_msg = "Text-to-Speech failed for some languages"
            print(f"⚠ {error_msg}")
            result['errors'].append(error_msg)
        
        result['audio_outputs'] = tts_result['audio_files']
        
        # Display audio outputs
        print(f"\n✓ Audio generation completed")
        for lang_name, audio_info in tts_result['audio_files'].items():
            if audio_info['success']:
                print(f"  {lang_name.capitalize()}: {audio_info['audio_path']} ({audio_info['file_size']:.2f} KB)")
            else:
                print(f"  {lang_name.capitalize()}: ✗ Failed")
        
        # Final result
        result['success'] = len(result['errors']) == 0
        result['processing_time'] = time.time() - start_time
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETED")
        print("="*60)
        print(f"Status: {'✓ SUCCESS' if result['success'] else '⚠ COMPLETED WITH ERRORS'}")
        print(f"Processing time: {result['processing_time']:.2f} seconds")
        print(f"Errors: {len(result['errors'])}")
        print("="*60)
        
        return result
    
    def get_summary(self, result):
        """
        Generate a summary of the pipeline result
        
        Args:
            result (dict): Pipeline result
            
        Returns:
            str: Formatted summary
        """
        summary = []
        summary.append("\n" + "="*60)
        summary.append("TRANSLATION SUMMARY")
        summary.append("="*60)
        
        # Input
        summary.append(f"\n📁 Input File: {result['input_file']}")
        summary.append(f"⏱️  Processing Time: {result['processing_time']:.2f} seconds")
        summary.append(f"📅 Timestamp: {result['timestamp']}")
        
        # Transcription
        if result['transcription']:
            summary.append(f"\n🎤 Original Speech (Chinese):")
            summary.append(f"   {result['transcription']['text']}")
            summary.append(f"   Confidence: {result['transcription']['confidence']:.2%}")
        
        # Translations
        if result['translations']:
            summary.append(f"\n🌐 Translations:")
            for lang_name, translation in result['translations'].items():
                if translation['success']:
                    summary.append(f"   {lang_name.capitalize()}: {translation['text']}")
                else:
                    summary.append(f"   {lang_name.capitalize()}: ✗ Failed")
        
        # Audio outputs
        if result['audio_outputs']:
            summary.append(f"\n🔊 Audio Outputs:")
            for lang_name, audio_info in result['audio_outputs'].items():
                if audio_info['success']:
                    summary.append(f"   {lang_name.capitalize()}: {audio_info['audio_path']}")
                else:
                    summary.append(f"   {lang_name.capitalize()}: ✗ Failed")
        
        # Errors
        if result['errors']:
            summary.append(f"\n⚠️  Errors ({len(result['errors'])}):")
            for error in result['errors']:
                summary.append(f"   - {error}")
        
        summary.append("\n" + "="*60)
        
        return "\n".join(summary)


# Test function
def test_pipeline():
    """Test the complete translation pipeline"""
    print("\n" + "="*60)
    print("Testing Complete Translation Pipeline")
    print("="*60)
    
    try:
        pipeline = TranslationPipeline()
    except Exception as e:
        print(f"\n✗ Pipeline initialization failed: {e}")
        return
    
    # Get audio file from user
    print("\n📁 Enter the path to your Chinese audio file")
    print("   (or press Enter to use: uploads/chinese_test.mp3)")
    
    audio_file = input("\nAudio file path: ").strip()
    
    if not audio_file:
        audio_file = "uploads/chinese_test.mp3"
        print(f"Using default: {audio_file}")
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"\n✗ File not found: {audio_file}")
        print(f"Current directory: {os.getcwd()}")
        return
    
    # Process the audio file
    result = pipeline.process_audio(
        audio_file_path=audio_file,
        source_language='zh-CN',
        target_languages=['en', 'bn']
    )
    
    # Display summary
    summary = pipeline.get_summary(result)
    print(summary)
    
    # Save result to JSON (optional)
    try:
        import json
        result_file = f"outputs/result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert result to JSON-serializable format
        json_result = {
            'success': result['success'],
            'input_file': result['input_file'],
            'transcription': result['transcription'],
            'translations': result['translations'],
            'audio_outputs': result['audio_outputs'],
            'processing_time': result['processing_time'],
            'timestamp': result['timestamp'],
            'errors': result['errors']
        }
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Result saved to: {result_file}")
        
    except Exception as e:
        print(f"\n⚠️  Could not save result to file: {e}")
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
    
    if result['success']:
        print("\n✓ All steps completed successfully!")
        print("\n📂 Check the outputs/ folder for:")
        print("   - English audio file")
        print("   - Bangla audio file")
        print("   - Result JSON file")
    else:
        print("\n⚠️  Pipeline completed with some errors")
        print(f"   {len(result['errors'])} error(s) occurred")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_pipeline()