import pyaudio
import wave
import requests
import time
from collections import deque
import threading
from numberizer import numberize

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer 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", "x-wait-for-model": "true"}

# Audio settings
CHUNK = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# We'll keep exactly 2 seconds of audio in our buffer.
SECONDS_TO_KEEP = 2
MAX_FRAMES = int(RATE / CHUNK * SECONDS_TO_KEEP)
global history
history = ""

# A text lookback buffer (if you still want to keep the last N transcriptions).
lookback_buffer = deque([])

def transcribe_audio(filename):
    """Send audio to HF Inference API (Whisper) and return transcription text."""
    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)

    try:
        result = response.json()
    except Exception as e:
        print("[!] Could not parse JSON response:", e)
        return ""

    if "text" in result:
        return result["text"]
    else:
        # Fallback if structure is different
        return str(result)


def register_new_transcription(buffer, new_transcription):
    """Keep track of the last 10 transcriptions in a buffer."""
    if len(buffer) >= 10:
        buffer.popleft()
    buffer.append(new_transcription)


def record_microphone(stream, p, filename="temp_audio.wav"):
    """
    Continuously read from the *already open* PyAudio stream.
    We store the incoming chunk in a ring buffer (`audio_buffer`),
    which always holds the last 2 seconds of audio data.

    Then we write those last 2 seconds to a WAV file and return its filename.
    """
    # Read a single chunk from the stream
    data = stream.read(int(RATE* 3), exception_on_overflow=False)

    # Now 'audio_buffer' has at most 2 seconds of audio (in CHUNK-sized frames).

    # Write the *entire* buffer (which is the last 2 seconds) to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

    return filename

def get_transcription(stream, p, i):
    global history
    # Get the most recent 2 seconds of audio as a WAV file
    temp_filename = f"temp_chunk{i}.wav"
    record_microphone(stream, p, filename=temp_filename)

    # Now transcribe
    transcription = transcribe_audio(temp_filename)
    if transcription.startswith(history):
        diff = transcription[len(history):]
    else:
        diff = transcription

    if "Gracias." in transcription or "Obrigado." in transcription or "Merci" in transcription:
        transcription = ""
    
    history = transcription
    # print(f"[*] Transcription ({temp_filename}): {transcription}")
    if diff:
        print(diff, flush=True)

    # # Optionally register in your lookback buffer
    register_new_transcription(lookback_buffer, transcription)

    i += 1

    # Avoid removing the file immediately if you want to debug;
    # otherwise, uncomment to clean up.
    # if os.path.exists(temp_filename):
    #     os.remove(temp_filename)

    return transcription


def main_loop():
    global history
    p = pyaudio.PyAudio()

    # Open the mic stream just once:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("[*] Starting the continuous microphone loop. Press Ctrl+C to exit.")

    i = 0
    try:
        while True:
            transcription = get_transcription(stream, p, i)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[*] Exiting transcription loop.")
    finally:
        # Properly close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    # Create and start the main loop in a thread
    main_thread = threading.Thread(target=main_loop, daemon=True)
    main_thread.start()

    print("[*] Main loop running in a thread. Press Ctrl+C to exit.")
    try:
        # Keep the main program running while the thread does its work
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Exiting the program.")
