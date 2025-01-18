import voice_control_v2 as vc
import browser
from gridify import to_alpha_numeric

clicking = False
typing = False

def populate_label_set(label_set):
    for i in range(0, 1000):
        label_set.add(to_alpha_numeric(i))

if __name__ == "__main__":
    label_set = set()
    populate_label_set(label_set)

    while True:
        # Record voice and return text at set intervals
        speech = "Please scroll down and click"
        speech = speech.lower()

        # Scan for keywords
        if "scroll up" in speech or "go up" in speech:
            browser.scroll_up()
        
        if "scroll down" in speech or "go down" in speech:
            browser.scroll_down()
        
        if not clicking and ("click" in speech or "tap" in speech or "press" in speech or "hit" in speech):
            vc.display_grid_image()
            clicking = True
        
        if clicking:
            # Check if we can find a grid label in this prompt
            for word in speech.split(" "):
                if word in label_set:
                    vc.click_at_cell(word)
                    vc.close_grid_image()
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
            cilcking = False
        
        if "enter" in speech or "return" in speech:
            browser.press_key("enter")
            typing = False

        if "exit" in speech or "quit" in speech or "terminate" in speech:
            break

        input("waiting...")
        clicking = False    # Test
        
        