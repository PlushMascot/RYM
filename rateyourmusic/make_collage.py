import os
from PIL import Image, ImageFont, ImageDraw, ImageColor


from settings import DIR, IMAGES_DIR


def make_collage(albums, output, n_rows, n_cols):
    if not albums:
        return 0

    im = Image.open(os.path.join(IMAGES_DIR, albums[0].id + ".jpg"))

    collage_width = n_cols * w
    collage_height = n_rows * h
    new_image = Image.new("RGB", (collage_width, collage_height))
    cursor = (0, 0)
    for album in albums:
        # place image
        path_to_album = os.path.join(IMAGES_DIR, album.id + ".jpg")
        new_image.paste(Image.open(path_to_album), cursor)

        # add name
        insert_name(new_image, " - ".join([album.artist, album.name]), cursor)

        # move cursor
        y = cursor[1]
        x = cursor[0] + w
        if cursor[0] >= (collage_width - w):
            y = cursor[1] + h
            x = 0
        cursor = (x, y)

    new_image.save(output)
    return 1


def insert_name(image, name, cursor):
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.truetype("Roboto-Black.ttf", size=17)
    x = cursor[0]
    y = cursor[1]
    draw.rectangle([(x, y + 200), (x + 300, y + 240)], (0, 0, 0, 123))
    draw.text((x + 8, y + 210), name, (255, 255, 255), font=font)
