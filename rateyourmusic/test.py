import random
from PIL import Image, ImageDraw, ImageFont
import requests
import sys
import urllib
from pprint import pprint


# def download_file(url, directory):
#     no = random.randint(1, 1000)
#     path = directory + "/" + "newfile+{no}.jpg".format(no=no)
#     urllib.request.urlretrieve(url, path)  # <-- This works now!
#     return path
#
#
# image_info = []
# for artist in artists:
#     url = artist["image"][3]["#text"]
#     path = download_file(url, "/Users/alairock/Desktop/demo")
#     spot_info = {
#         "name": artist["name"],
#         "path": path,
#     }
#     image_info.append(spot_info)


def insert_name(image, name, cursor):
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.truetype("myfont.ttf", size=17)
    x = cursor[0]
    y = cursor[1]
    draw.rectangle([(x, y + 200), (x + 300, y + 240)], (0, 0, 0, 123))
    draw.text((x + 8, y + 210), name, (255, 255, 255), font=font)


def create_collage(cells, cols=3, rows=3):
    w, h = Image.open(image_info[0]["path"]).size
    collage_width = cols * w
    collage_height = rows * h
    ims = []
    new_image = Image.new("RGB", (collage_width, collage_height))
    cursor = (0, 0)
    for cell in cells:
        # place image
        new_image.paste(Image.open(cell["path"]), cursor)

        # add name
        insert_name(new_image, cell["name"], cursor)

        # move cursor
        y = cursor[1]
        x = cursor[0] + w
        if cursor[0] >= (collage_width - w):
            y = cursor[1] + h
            x = 0
        cursor = (x, y)

    new_image.save("Collage.jpg")
