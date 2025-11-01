import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

print("=" * 50)
print("Testing Google Cloud API Configuration")
print("=" * 50)

if api_key:
    print(f"✓ API Key loaded: {api_key[:20]}...")
else:
    print("✗ API Key not found!")

if project_id:
    print(f"✓ Project ID: {project_id}")
else:
    print("✗ Project ID not found!")

print("=" * 50)
print("\nTesting API connections...")

# Test Speech-to-Text
try:
    from google.cloud import speech
    print("✓ Speech-to-Text library imported successfully")
except Exception as e:
    print(f"✗ Speech-to-Text error: {e}")

# Test Translation
try:
    from google.cloud import translate_v2 as translate
    print("✓ Translation library imported successfully")
except Exception as e:
    print(f"✗ Translation error: {e}")

# Test Text-to-Speech
try:
    from google.cloud import texttospeech
    print("✓ Text-to-Speech library imported successfully")
except Exception as e:
    print(f"✗ Text-to-Speech error: {e}")

print("=" * 50)
print("\nSetup check complete!")
print("If all checks passed (✓), you're ready to proceed!")