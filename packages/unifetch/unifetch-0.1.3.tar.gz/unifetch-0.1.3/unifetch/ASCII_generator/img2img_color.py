"""
Based on the ascii-generator module (https://github.com/uvipen/ASCII-generator)

Used under MIT License (https://github.com/uvipen/ASCII-generator/blob/master/LICENSE)

@author: Viet Nguyen <nhviet1009@gmail.com>
@author: Luke Briggs <contact@lukebriggs.dev>
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from .utils import get_data

from functools import partial


def to_rgb(color):
    return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF


target_colors = {
    0x000000: "\33[30m",  # black
    0x990000: "\33[31m",  # red
    0x00A600: "\33[32m",  # green
    0x999900: "\33[33m",  # yellow
    0x0000B2: "\33[34m",  # blue
    0xB200B2: "\33[35m",  # magenta
    0x00A6B2: "\33[36m",  # cyan
    0xBFBFBF: "\33[37m",  # white
    0x222222: "\33[30m",  # bright black
    0xE50000: "\33[31m",  # bright red
    0x00D900: "\33[32m",  # bright green
    0xE5E500: "\33[33m",  # bright yellow
    0x0000FF: "\33[34m",  # bright blue
    0xE500E5: "\33[35m",  # bright magenta
    0x00E5E5: "\33[36m",  # bright cyan
    0xE5E5E5: "\33[37m",  # bright white
}


def euclidian(c1, c2):
    r, g, b = to_rgb(c1)
    s, h, c = to_rgb(c2)
    r -= s
    g -= h
    b -= c
    return r * r + g * g + b * b


def closest_color(color, target_colors=target_colors, dist=euclidian):
    return min(target_colors, key=partial(dist, color))

def process_image(image, background, num_cols):
    if background == "white":
        bg_code = (255, 255, 255)
    else:
        bg_code = (0, 0, 0)
    char_list, font, sample_character, scale = get_data()
    char_list = '@%#*+=-:. '
    num_chars = len(char_list)
    image = cv2.imread(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    cell_width = width / num_cols
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    char_width, char_height = font.getsize(sample_character)
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    ansi_text = ""
    for i in range(num_rows):
        ansi_text += "\n"
        for j in range(num_cols):
            partial_image = image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                            int(j * cell_width):min(int((j + 1) * cell_width), width), :]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            hex_color=int('0x%02x%02x%02x' % partial_avg_color, 16)
            bestmatch = closest_color(hex_color)
            code = target_colors[bestmatch]
            char = char_list[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            ansi_text += code + char + "\33[0m"
            draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)

    if background == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
    else:
        cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    return ansi_text, out_image


def get_text(image, background="black", num_cols=32):
    return process_image(image, background, num_cols)[0]


def get_image(image, background="black", num_cols=45):
    return process_image(image, background, num_cols)[1]