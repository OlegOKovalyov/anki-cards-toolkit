from pydub import AudioSegment
import os

def generate_silence(duration_ms=1000, filename="silence_1sec.mp3"):
    """Generate a silent MP3 file of specified duration."""
    silence = AudioSegment.silent(duration=duration_ms)
    silence.export(filename, format="mp3")
    print(f"Generated {filename} ({duration_ms/1000} seconds of silence)")

if __name__ == "__main__":
    generate_silence() 