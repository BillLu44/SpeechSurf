import voice_control_v2 as vc
import browser
from gridify import to_alpha_numeric
from final_transcriber import get_transcription, CHUNK, FORMAT, CHANNELS, RATE
import time
import pyaudio
import threading
from numberizer import numberize

clicking = False
typing = False

def populate_label_set(label_set):
    for i in range(0, 1000):
        label_set.add(to_alpha_numeric(i))

if __name__ == "__main__":
    label_set = set()
    populate_label_set(label_set)

    global history, suspended
    suspended = False
    p = pyaudio.PyAudio()

    # Open the mic stream just once:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("[*] Starting the continuous microphone loop. Press Ctrl+C to exit.")

    history_i = 0   
    i = 0
    # grid_thread = threading.Thread(target=vc.display_grid_image, daemon=True)

    while True:
        # Record voice and return text at set intervals
        speech = get_transcription(stream, p, i, history_i)
        speech = speech.lower()
        print(clicking, "clicking")

        if not suspended and "suspend" in speech:
            suspended = True
            continue

        elif suspended:
            if "prolong" in speech:
                suspended = False
            continue

        # Scan for keywords
        if "scroll up" in speech or "go up" in speech:
            browser.scroll_up()
        
        elif "scroll down" in speech or "go down" in speech:
            browser.scroll_down()
        
        elif not clicking and ("click" in speech or "tap" in speech or "press" in speech or "hit" in speech):
            grid_thread = threading.Thread(target=vc.display_grid_image, daemon=True)
            grid_thread.start()
            clicking = True
        
        elif not clicking and ("resume" in speech or "pause" in speech or "freeze" in speech):
            browser.pause()

        elif not clicking and "backward" in speech or "previous" in speech:
            browser.fast_backward()

        elif not clicking and "forward" in speech or "next" in speech:
            browser.fast_forward()

        if clicking:
            # Check if we can find a grid lab in this prompt
            for label in label_set:
                if str(int(label)) in numberize(speech).split(" "):
                    print("Label:", str(int(label)))
                    vc.close_grid_image()
                    vc.click_at_cell(label)
                    clicking = False
                    break

        if "type" in speech or "write" in speech:
            typing = True
            type_text = ""

            if "type" in speech:
                type_text = speech[(speech.find("type") + 4):]
            else:
                type_text = speech[(speech.find("write") + 5):]

            browser.type_text(type_text)

        if typing:
            browser.type_text(speech)

        if "stop" in speech or "cancel" in speech or "never mind" in speech:
            typing = False
            vc.close_grid_image()
            clicking = False
        
        if "enter" in speech or "return" in speech:
            browser.press_key("enter")
            typing = False

        if "exit" in speech or "quit" in speech or "terminate" in speech:
            break
        
        # clicking = False    # Test
    
    # Properly close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
        
# 