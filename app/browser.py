import pyautogui as auto
import keyboard
import time

TYPING_INTERVAL = 0.01  # How many seconds between key presses
SCROLL_AMOUNT = 30       # How many "clicks" of the scroll wheel

# Global vars
screenshot_num = 0

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

def type_text(text):
    for char in text:
        if char.isupper():
            auto.keyDown("shift")
            auto.typewrite(char, interval=TYPING_INTERVAL)
            auto.keyUp("shift")
        else:
            auto.typewrite(char, interval=TYPING_INTERVAL)
    
    auto.press("enter")

def take_screenshot():
    global screenshot_num
    screenshot_num += 1
    print("Taking screenshot...")
    auto.screenshot("images/screenshot_" + str(screenshot_num) + ".png")

def scroll_up():
    auto.scroll(SCROLL_AMOUNT)

def scroll_down():
    auto.scroll(-SCROLL_AMOUNT)

def press_key(key):
    auto.press(key)

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

