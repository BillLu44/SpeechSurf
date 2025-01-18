import gridify, browser
import time
import tkinter as tk
from PIL import Image, ImageTk

cell_dict = {}
image_running = False

# Tkinter binded function
def on_destroy(event):
    if event.widget == root:
        print("closed")
        close_grid_image()

def full_screen_image(pilImage):
    global root, image_running

    root = tk.Toplevel()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit(), on_destroy(e)))
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
    image_running = True
    root.mainloop()

def display_grid_image():
    browser.take_screenshot()
    
    global cell_dict
    cell_dict, grid_image = gridify.gridify(browser.screenshot_num)
    grid_ss_path = f"images/screenshot_{browser.screenshot_num}_grid.png"

    # Display the grid image in full screen
    full_screen_image(grid_image)

def close_grid_image():
    global image_running

    if image_running:
        print("QUITTING tkinter")
        root.quit()
        image_running = False

def click_at_cell(cell_label):
    browser.slow_left_click(cell_dict[cell_label][0], cell_dict[cell_label][1], 1)
