import pyautogui as auto
import keyboard
import time
import threading

TYPING_INTERVAL = 0.01  # How many seconds between key presses

# Global vars
screenshot_num = 0
text = ""

# Functions
def move_to(x, y, moveDuration):
    auto.moveTo(x, y, duration=moveDuration)

def slow_left_click(x, y, moveDuration):
    auto.moveTo(x, y, duration=moveDuration)
    auto.click()

def fast_left_click(x, y):
    auto.click(x, y)

def slow_right_click(x, y, moveDuration):
    auto.moveTo(x, y, duration=moveDuration)
    auto.rightClick()

def fast_right_click(x, y):
    auto.rightClick(x, y)

def slow_double_click(x, y, moveDuration):
    auto.moveTo(x, y, duration=moveDuration)
    auto.leftClick()
    auto.leftClick()

def fast_double_click(x, y):
    auto.leftClick(x, y)
    auto.leftClick(x, y)

def type_text(new_text):
    global text
    text = new_text
    thread = threading.Thread(target=type_text_real, daemon=True)
    thread.start()
    thread.join()

def type_text_real():
    for char in text:
        if char.isupper():
            auto.keyDown("shift")
            auto.write(char)
            auto.keyUp("shift")
        else:
            auto.write(char)

def take_screenshot():
    global screenshot_num
    screenshot_num += 1
    print("Taking screenshot...")
    auto.screenshot("images/screenshot_" + str(screenshot_num) + ".png")

def scroll_up(amount):
    auto.scroll(amount)

def scroll_down(amount):
    auto.scroll(-amount)

def press_key(key):
    auto.press(key)

def fast_forward():
    auto.press('right')

def fast_backward():
    auto.press("left")

def pause():
    auto.press('k') 

if __name__ == "__main__":
    time.sleep(2)
    fast_right_click(500, 630)
    slow_left_click(600, 610, 0.5)
    time.sleep(1)
    slow_left_click(1450, 240, 1)
    slow_left_click(1500, 300, 1)
    fast_left_click(None, None)
    fast_left_click(None, None)
    type_text("Chem Eng Student @ University of Waterloo")
    auto.press("enter")

