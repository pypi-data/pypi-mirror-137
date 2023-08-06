import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
import os

def sort_chars(char_list, font):
    char_width, char_height = font.getsize("A")
    num_chars = min(len(char_list), 100)
    out_width = char_width * len(char_list)
    out_height = char_height
    out_image = Image.new("L", (out_width, out_height), 255)
    draw = ImageDraw.Draw(out_image)
    draw.text((0, 0), char_list, fill=0, font=font)
    cropped_image = ImageOps.invert(out_image).getbbox()
    out_image = out_image.crop(cropped_image)
    brightness = [np.mean(np.array(out_image)[:, 10 * i:10 * (i + 1)]) for i in range(len(char_list))]
    char_list = list(char_list)
    zipped_lists = zip(brightness, char_list)
    zipped_lists = sorted(zipped_lists)
    result = ""
    counter = 0
    incremental_step = (zipped_lists[-1][0] - zipped_lists[0][0]) / num_chars
    current_value = zipped_lists[0][0]
    for value, char in zipped_lists:
        if value >= current_value:
            result += char
            counter += 1
            current_value += incremental_step
        if counter == num_chars:
            break
    if result[-1] != zipped_lists[-1][1]:
        result += zipped_lists[-1][1]
    return result


def get_data():
    font = ImageFont.truetype(os.path.dirname(__file__) + "/fonts/DejaVuSansMono-Bold.ttf", size=20)
    sample_character = "A"
    scale = 2
    char_list = sort_chars("@%#*+=-:. ", font)

    return char_list, font, sample_character, scale
