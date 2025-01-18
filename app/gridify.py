from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import math

# Define a function to convert the cell index to alphanumeric
def to_alpha_numeric(index):
    if index < 1000:
        return f"{index:03d}"  # 3 digit number with leading zeros
    else:
        index -= 1000  # Adjust index as we start from 1000 for alphabetic
        return f"{chr(65 + index // 100)}{index % 100:02d}"  # Alphabetic prefix with 2 digit number

# Function to add an alphanumeric grid to an image
def add_alpha_numeric_grid_to_image(base_image_path, output_path, cell_size=100, grid_color='black', text_opacity=128, text_offset_x=5, label_background_color=(255, 255, 255, 128), font_size=20):
    # Open the base image
    base_image = Image.open(base_image_path).convert("RGBA")

    # Create a new transparent image for the grid and text
    txt = Image.new('RGBA', base_image.size, (255, 255, 255, 0))

    font = ImageFont.truetype("arial.ttf", font_size)

    # Get a drawing context for the grid and text overlay
    d = ImageDraw.Draw(txt)

    # Calculate the number of grid lines needed based on the cell size
    num_x_cells = base_image.width // cell_size
    num_y_cells = base_image.height // cell_size

    # Make a dict of type str -> (int, int) which maps a cell's alphanumeric value to the coordinates of its center
    cell_dict = {}

    # Draw the grid lines and the numbers
    for y in range(num_y_cells):  # Include an extra cell for the partial row
        for x in range(num_x_cells):  # Include an extra cell for the partial column

            # Calculate the adjusted cell size
            adjusted_cell_size_x = base_image.width / num_x_cells
            adjusted_cell_size_y = base_image.height / num_y_cells
            adjusted_cell_size = min(adjusted_cell_size_x, adjusted_cell_size_y)

            # Calculate the position for each cell
            top_left_x = x * adjusted_cell_size
            top_left_y = y * adjusted_cell_size
            bottom_right_x = min(top_left_x + adjusted_cell_size, base_image.width)  # Ensure we do not go beyond the image width by more than a cell
            bottom_right_y = min(top_left_y + adjusted_cell_size, base_image.height)  # Ensure we do not go beyond the image height by more than a cell
            
            # Calculate the center of each grid cell
            center_x = (x * adjusted_cell_size) + (adjusted_cell_size / 2)
            center_y = (y * adjusted_cell_size) + (adjusted_cell_size / 2)

            # Draw the semi-transparent background rectangle for the label
            d.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], fill=label_background_color)

            # Drawing the grid lines
            d.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], outline=grid_color)

            # Creating the alphanumeric label for each cell
            label = to_alpha_numeric(x + y * num_x_cells)

            # Calculate text position
            text_x = (top_left_x + bottom_right_x) / 2 - text_offset_x
            text_y = (top_left_y + bottom_right_y) / 2

            # Drawing the label in the middle of the cell
            d.text((text_x, text_y), label, fill=(0, 0, 0, text_opacity), font=font, anchor="mm")

            # Save this cell along with its center coordinates into the dict
            cell_dict[label] = (center_x, center_y)

    # Composite the base image with the grid and text overlay
    combined = Image.alpha_composite(base_image, txt)

    # Save or show the final image
    combined = combined.convert("RGB")  # Remove alpha for saving in jpg format.
    combined.save(output_path)
    # combined.show()

    # Return the cell dict and gridified image
    return cell_dict, combined

# Function to draw a red circle at the center of each grid cell
def draw_red_circle_on_grid(image_path, output_path, tar_cell, cell_size=100, circle_color='red', circle_radius=10,):
    # Open the base image
    base_image = Image.open(image_path).convert("RGBA")

    # Create a drawing context
    draw = ImageDraw.Draw(base_image)

    # Calculate the number of grid lines
    num_x_cells = base_image.width // cell_size
    num_y_cells = base_image.height // cell_size

    # Draw a red circle at the center of each grid cell
    for y in range(num_y_cells):
        for x in range(num_x_cells):
            # Calculate the center of each grid cell
            center_x = (x * cell_size) + (cell_size / 2)
            center_y = (y * cell_size) + (cell_size / 2)

            # Draw the circle
            cell = int(to_alpha_numeric(x + y * num_x_cells))
            print(cell)
            if cell == tar_cell:
                draw.ellipse(
                    [
                        (center_x - circle_radius, center_y - circle_radius),
                        (center_x + circle_radius, center_y + circle_radius)
                    ],
                    fill=circle_color
                )

    # Save or show the final image
    base_image = base_image.convert("RGB")
    base_image.save(output_path)
    # base_image.show()

def gridify(screenshot_num):
    # Set the paths for the base image and the output images
    base_image_path = f'images/screenshot_{screenshot_num}.png'  # Update to your image file
    grid_output_path = f'images/screenshot_{screenshot_num}_grid.png'

    # Call the functions
    cell_dict, grid_image = add_alpha_numeric_grid_to_image(base_image_path, grid_output_path, cell_size=52)
    # draw_red_circle_on_grid(grid_output_path, circle_output_path, tar_cell=340, cell_size=100)

    return cell_dict, grid_image
