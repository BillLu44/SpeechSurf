from openai import OpenAI
client = OpenAI()
import browser
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image("images/screenshot_1.png")

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here is a screenshot. I want to use pyautogui to click on the Google search bar in this screenshot. The full screen size is 1920 x 1080. Can you give me the coordinates that I would click into? Do not output anything else, just the coordinates in the form [x, y] without the square brackets. Please verify your answer 3 times by checking if the search bar really is being clicked at those coordinates, then give me your final answer."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ],
        }
    ]
)

output = completion.choices[0].message.content.split(", ")

print(output[0])
print(output[1])

browser.slow_left_click(int(output[0]), int(output[1]), 1)