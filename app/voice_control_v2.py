import gridify, browser
import time
import tkinter as tk
from PIL import Image, ImageTk

def full_screen_image(pilImage):
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tk.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()


time.sleep(2)
browser.take_screenshot()

cell_dict, grid_image = gridify.gridify(browser.screenshot_num)
grid_ss_path = f"images/screenshot_{browser.screenshot_num}_grid.png"

# Display the grid image in full screen
full_screen_image(grid_image)

# Click on this cell
cell_label = input("Where to click? ")
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("Clicking...")
browser.slow_left_click(cell_dict[cell_label][0], cell_dict[cell_label][1], 1)

