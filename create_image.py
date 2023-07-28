import os
import roman
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor
from constants import *
mc_font_file = "assets/MinecraftRegular-Bmg3.ttf"

def gen_card(data):
    ic_size = 100

    print(data)
    with Image.open("assets/background.png") as img_bg:
        img_bg.load()
    bg_width, bg_height = img_bg.size
    img_font = Image.new("RGBA", img_bg.size)
    ic_file = "assets/icons/" + data["display_name"].replace(" ", "_") + ".png"
    if os.path.exists(ic_file):
        with Image.open(ic_file) as img_ic:
            img_ic.load()
    else:
        with Image.open("assets/icons/Cactus.png") as img_ic:
            img_ic.load()
    img_ic = img_ic.convert("RGBA")
    with Image.open("assets/bar.png") as img_bar:
        img_bar.load()

    with Image.open("assets/bar_full.png") as img_bar_full:
        img_bar_full.load()

    # bar
    if "percentage_to_next_tier" not in data:
        data["percentage_to_next_tier"]=0
    img_bar_full = img_bar_full.crop(
        (0, 0, int(img_bar_full.size[0] * data["percentage_to_next_tier"]), img_bar_full.size[1]))

    img_ic = img_ic.resize((ic_size, ic_size))
    main_y_dis = bg_height + 15
    # text
    font_size = 20
    if data["maxed_out"]:
        missing = "DONE"
        missing_color=ImageColor.getrgb("#55FF55")
    else:
        missing_color=ImageColor.getrgb("#FF5555")
        missing = "-" + str(data["missing_to_next_tier"])
    bb_length = img_bar.size[0]
    mc_font = ImageFont.truetype(mc_font_file, font_size)
    if data["tier_now"] == 0:
        lvl="0"
    else:
        lvl = roman.toRoman(data["tier_now"])
    s = data["display_name"] + " " + lvl
    t = s + missing + "  "
    while mc_font.getbbox(t)[2] < (bb_length) and mc_font.getbbox(t)[3] < (50):
        font_size += 1
        mc_font = ImageFont.truetype(mc_font_file, font_size)

    y_plus = mc_font.getbbox(t)[3]
    draw = ImageDraw.Draw(img_font)
    draw.text((0, 0), s, (255, 255, 255), font=mc_font)
    missing_size = mc_font.getbbox(missing)[2]
    draw.text((bb_length - missing_size, 0), missing, missing_color, font=mc_font)
    print(font_size)
    # composite
    y_distance = (bg_height - ic_size) // 2
    try:
        img_bg.alpha_composite(img_ic, (40, y_distance))
        img_bg.alpha_composite(img_bar, (main_y_dis, 92))
        img_bg.alpha_composite(img_bar_full, (main_y_dis, 92))
        img_bg.alpha_composite(img_font, (main_y_dis, y_distance - 5 + ((75 - y_plus) // 2)))
    except:
        print(data["display_name"])
        print(img_bg,img_ic)
        img_bg.show()
        img_ic.show()
    return img_bg


if __name__ == '__main__':
    for d in read_from_json("/home/aws1313/Downloads/localhost.json")["sorted"]:
        if "display_name" in d.keys():
            gen_card(d).save("temp/"+d["display_name"]+".png")

