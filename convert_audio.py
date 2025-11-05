#!/usr/bin/env python3
"""
Audio File Converter for Translation Pipeline
Converts audio files to formats that work best with Google Speech-to-Text
"""

import sys
import os

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    import shutil
    return shutil.which('ffmpeg') is not None

def convert_to_flac(input_file, output_file=None):
    """
    Convert audio file to FLAC format (best for Google Speech-to-Text)

    Args:
        input_file: Path to input audio file
        output_file: Path for output file (optional)

    Returns:
        Path to converted file
    """
    if not check_ffmpeg():
        print("ERROR: ffmpeg is not installed")
        print("\nInstall ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  Mac: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return None

    if output_file is None:
        base = os.path.splitext(input_file)[0]
        output_file = f"{base}_converted.flac"

    # Convert to FLAC with optimal settings for speech recognition
    # - Mono channel (better for speech)
    # - 16kHz sample rate (optimal for Google)
    # - FLAC encoding (lossless, works best)

    import subprocess

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-ac', '1',  # Convert to mono
        '-ar', '16000',  # 16kHz sample rate
        '-y',  # Overwrite output file
        output_file
    ]

    print(f"Converting {input_file} to FLAC format...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / 1024
            print(f"✓ Conversion successful!")
            print(f"✓ Output: {output_file} ({file_size:.2f} KB)")
            return output_file
        else:
            print(f"✗ Conversion failed!")
            print(f"Error: {result.stderr}")
            return None

    except Exception as e:
        print(f"✗ Conversion error: {e}")
        return None

def get_audio_info(file_path):
    """Get information about audio file"""
    if not check_ffmpeg():
        return None

    import subprocess
    import json

    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        file_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'streams' in data and len(data['streams']) > 0:
                stream = data['streams'][0]
                return {
                    'codec': stream.get('codec_name', 'unknown'),
                    'sample_rate': stream.get('sample_rate', 'unknown'),
                    'channels': stream.get('channels', 'unknown'),
                    'duration': stream.get('duration', 'unknown'),
                    'bit_rate': stream.get('bit_rate', 'unknown')
                }
    except:
        pass

    return None

def main():
    """Main conversion function"""
    print("="*60)
    print("Audio File Converter for Translation Pipeline")
    print("="*60)

    if len(sys.argv) < 2:
        print("\nUsage: python convert_audio.py <input_file> [output_file]")
        print("\nExample:")
        print("  python convert_audio.py myaudio.mp3")
        print("  python convert_audio.py myaudio.mp3 output.flac")
        print("\nSupported input formats: MP3, WAV, M4A, OGG, WEBM, etc.")
        print("Output format: FLAC (optimized for speech recognition)")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"✗ Error: File not found: {input_file}")
        sys.exit(1)

    # Get audio info
    print(f"\n📁 Input file: {input_file}")
    print(f"📏 Size: {os.path.getsize(input_file) / 1024:.2f} KB")

    info = get_audio_info(input_file)
    if info:
        print(f"\n📊 Audio Information:")
        print(f"  Codec: {info['codec']}")
        print(f"  Sample Rate: {info['sample_rate']} Hz")
        print(f"  Channels: {info['channels']}")
        print(f"  Duration: {info['duration']} seconds")
        print(f"  Bit Rate: {info['bit_rate']} bps")

        # Check if conversion is needed
        needs_conversion = False
        reasons = []

        if info['sample_rate'] != '16000':
            needs_conversion = True
            reasons.append(f"Sample rate is {info['sample_rate']} Hz (should be 16000 Hz)")

        if info['channels'] != '1':
            needs_conversion = True
            reasons.append(f"Audio is {['unknown', 'mono', 'stereo'][int(info['channels'])]} (should be mono)")

        if info['codec'] not in ['flac', 'pcm_s16le']:
            needs_conversion = True
            reasons.append(f"Codec is {info['codec']} (FLAC works best)")

        if needs_conversion:
            print(f"\n⚠️  Conversion recommended:")
            for reason in reasons:
                print(f"  - {reason}")
        else:
            print(f"\n✓ File already in optimal format!")
            print(f"  You can upload this file directly.")
            return

    print(f"\n🔄 Converting to optimal format...")
    print(f"  - Format: FLAC")
    print(f"  - Sample Rate: 16000 Hz")
    print(f"  - Channels: Mono")
    print()

    # Convert
    result = convert_to_flac(input_file, output_file)

    if result:
        print(f"\n✅ SUCCESS! Upload this file to the webapp:")
        print(f"   {result}")
        print(f"\nThis file should work much better with speech recognition!")
    else:
        print(f"\n❌ CONVERSION FAILED")
        print(f"\nAlternative: Try using an online converter:")
        print(f"  1. Go to: https://cloudconvert.com/mp3-to-flac")
        print(f"  2. Upload your file")
        print(f"  3. Set: Sample Rate = 16000 Hz, Channels = Mono")
        print(f"  4. Convert and download")
        print(f"  5. Upload to webapp")

if __name__ == "__main__":
    main()
