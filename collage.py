import os
from PIL import Image


DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(DIR, "images")


def make_collage(pics, filename):
    if not pics:
        print("I couldnt get any pictures:(")
        return
