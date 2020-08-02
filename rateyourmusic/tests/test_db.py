from src.db import db_insert_image
from src.album_object import Album
import pytest
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_db_insert_image():
    album = Album(
        artist="Vanessa Amara",
        name="Manos",
        link="https://rateyourmusic.com/release/album/vanessa-amara/manos/",
        id="Album8969191",
        file_path=os.path.abspath(os.path.join(DIR, "images", id + ".jpg")),
    )
    assert db_insert_image(album) == 1
