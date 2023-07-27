import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import numpy as np
from constants import *

if __name__ == '__main__':
    data = read_from_json("/home/aws1313/Downloads/localhost.json")["sorted"][0]
    mc_font = ImageFont.truetype("assets/MinecraftRegular-Bmg3.otf", 20)
    ic_size = 120

    print(data)
    with Image.open("assets/background.png") as img_bg:
        img_bg.load()
    bg_width, bg_height = img_bg.size
    with Image.open("assets/Carrot.webp") as img_ic:
        img_ic.load()

    with Image.open("assets/bar.png") as img_bar:
        img_bar.load()

    img_ic = img_ic.resize((ic_size, ic_size))
    img_bg.alpha_composite(img_ic, (20,(bg_height-ic_size)//2))
    img_bg.alpha_composite(img_bar, (150,92))
    draw = ImageDraw.Draw(img_bg)
    draw.text((0, 0), "Sample Text", (255, 255, 255), font=mc_font)

    img_bg.show()
