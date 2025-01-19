import voice_control_v2 as vc
import browser
from gridify import to_alpha_numeric
from final_transcriber import get_transcription, CHUNK, FORMAT, CHANNELS, RATE
import pyaudio
import threading
from numberizer import numberize
import sys

left_clicking = False
right_clicking = False
double_clicking = False
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

    i = 0
    # grid_thread = threading.Thread(target=vc.display_grid_image, daemon=True)

    while True:
        # Record voice and return text at set intervals
        speech = get_transcription(stream, p, i)
        speech = speech.lower()
        print(left_clicking or right_clicking or double_clicking, "clicking")

        if not suspended and "suspend" in speech:
            suspended = True
            continue

        elif suspended:
            if "prolong" in speech:
                suspended = False
            continue

        # Scan for keywords
        if "scroll up a lot" in speech or "scroll up more" in speech:
            browser.scroll_up(1000)

        elif "scroll up" in speech or "go up" in speech:
            browser.scroll_up(600)

        elif "scroll down a lot" in speech or "scroll down more" in speech:
            browser.scroll_down(1000)
        
        elif "scroll down" in speech or "go down" in speech:
            browser.scroll_down(600)
        
        elif (not right_clicking and not left_clicking and not double_clicking):
            if "right click" in speech:
                grid_thread = threading.Thread(target=vc.display_grid_image, daemon=True)
                grid_thread.start()
                right_clicking = True

            elif "double click" in speech:
                grid_thread = threading.Thread(target=vc.display_grid_image, daemon=True)
                grid_thread.start()
                double_clicking = True
            
            elif "click" in speech or "tap" in speech or "press" in speech or "hit" in speech:
                grid_thread = threading.Thread(target=vc.display_grid_image, daemon=True)
                grid_thread.start()
                left_clicking = True
            
            elif "resume" in speech or "pause" in speech or "freeze" in speech:
                browser.pause()

            elif "backward" in speech or "previous" in speech:
                browser.fast_backward()

            elif "forward" in speech or "next" in speech:
                browser.fast_forward()

        if left_clicking or right_clicking or double_clicking:
            # Check if we can find a grid lab in this prompt
            for label in label_set:
                if str(int(label)) in numberize(speech).split(" "):
                    print("Label:", str(int(label)))
                    vc.close_grid_image()

                    if left_clicking:
                        vc.left_click_at_cell(label)
                        left_clicking = False
                    elif right_clicking:
                        vc.right_click_at_cell(label)
                        right_clicking = False
                    elif double_clicking:
                        vc.double_click_at_cell(label)
                        double_clicking = False
                    break

        if "stop" in speech or "cancel" in speech or "never mind" in speech:
            typing = False
            left_clicking = False
            right_clicking = False
            double_clicking = False
            vc.close_grid_image()

        if "enter" in speech or "return" in speech:
            browser.press_key("enter")
            typing = False

        if "exit" in speech or "terminate" in speech:
            break
        
        if typing:
            browser.type_text(speech)

        if "type" in speech or "write" in speech:
            typing = True
            type_text = ""

            if "type" in speech:
                type_text = speech[(speech.find("type") + 5):]
            else:
                type_text = speech[(speech.find("write") + 6):]

            print("Type text:", type_text)

            browser.type_text(type_text)
        
        # clicking = False    # Test
    
    # Properly close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    sys.exit(0)
        
# 