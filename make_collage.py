import os
from PIL import Image


DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(DIR, "images")


def make_collage(pics, output, n_rows, n_cols):
    if not pics:
        return 0
