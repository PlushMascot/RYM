"""
explanation of url params:
https://rateyourmusic.com/wiki/Sandbox:Links
"""
import argparse
import bs4
import requests
import json
import os
import time
import shutil
import random
import re

from PIL import Image
from typing import Any, List

from album_object import Album
from db import db_insert_image
from settings import (
    DIR,
    IMAGES_DIR,
    RYM_URL,
    ALBUMS_PER_PAGE,
    HTTP_headers,
    LAST_API_KEY,
)


def parse_user_collection(username: str, stars: List[float]) -> List[Any]:
    """
    Figures out what albums in user's collection fit the criteria.
    Fetches necessary information about those albums.

    Returns: list of namedtuple("Album", ["artist", "name", "link", "id", "file_path"])
    """

    collection_url = (
        f"{RYM_URL}/collection/{username}/"
        f"d.rp,a,l,aat,r{min(stars)}-{max(stars)},n{ALBUMS_PER_PAGE}/"
    )

    user_url = RYM_URL + f"~{username}"
    albums_to_scan = get_num_of_albums(user_url, stars)
    if albums_to_scan == 0:
        return []

    pages_to_scan = albums_to_scan // ALBUMS_PER_PAGE + 1
    albums_data = []
    for page in range(1, pages_to_scan + 1):
        albums_data.extend(get_chunk_of_collection(collection_url + f"{page}"))

    return albums_data


def get_num_of_albums(user_url: str, stars: List[str]) -> int:
    """
    Counts how many albums in total user had rated within the range of {stars}.
    Analyzing rateyourmusic.com/{username} html.
    """

    response = requests.get(user_url, headers=HTTP_headers)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    table_div = soup.find("div", {"id": "musicrating"})
    table = table_div.find("table", attrs={"class": "mbgen"})

    popssible_ratings = [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5]
    number_of_reviews = {key: 0 for key in popssible_ratings}
    for row, key in zip(table.find_all("tr")[1:], range(len(popssible_ratings))):
        column = row.find("b")  # number of reviews with rating [5.0 ... 0.5]
        if column:
            text_value = column.text
            number_of_reviews[key] = int(text_value.replace(",", ""))

    albums_to_scan = 0
    for star in popssible_ratings:
        if star in stars:
            albums_to_scan += number_of_reviews[star]
    return albums_to_scan


def get_chunk_of_collection(link: str) -> List:
    """
    scrapes album info from users collection from a page

    Returns: list of namedtuple("Album", ["artist", "name", "link", "id", "file_path"]), e.g.
        [
        {
         'artist': 'The Beatles'
         'album': 'Yellow Submarine Songtrack',
         'link': '/release/comp/the-beatles/yellow-submarine-songtrack/',
         'id': '261',
         'file_path': 'C:\\Images\\1.jpg'
        }
        ]
    """

    chunk_of_albums = []
    response = requests.get(link, headers=HTTP_headers)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    table = soup.find("table", attrs={"class": "mbgen"})

    for row in table.find_all("tr")[1:]:  # fiirst row is the table header
        artists = row.find_all("a", attrs={"class": "artist"})
        artist = " & ".join(a.text for a in artists)

        album_name = row.find("a", attrs={"class": "album"}).text
        relative_album_link = row.find("a", attrs={"class": "album"}).get("href")

        text_id = row.find("a", attrs={"class": "album"}).get("title")
        id = re.findall(r"\d+", text_id)[0]

        file_path = os.path.join(IMAGES_DIR, id + ".jpg")

        album = Album(artist, album_name, RYM_URL.rstrip("/") + relative_album_link, id)
        chunk_of_albums.append(album)
    return chunk_of_albums


def ensure_download(albums, n: int) -> List:
    """
    downloads images if there is no aldready
    randomly picks n images out of {len(album_data)}

    Returns: list of namedtuple("Album", ["artist", "name", "link", "id", "file_path"])
    """
    for album in albums:
        if not cached(album):
            downloaded = download_image_from_rym(album)
            # downloaded = download_image_from_last(album)
            if not downloaded:
                albums.remove(album)
            db_insert_image(album)

    return random.sample(albums, n)


def download_image_from_rym(album):
    time.sleep(2 * random.random() + 1)  # do not download too fast

    album_link, filename = album.link, album.id + ".jpg"
    try:
        response = requests.get(album_link, headers=HTTP_headers)
        soup = bs4.BeautifulSoup(response.text, features="html.parser")
        cover_link = "https:" + soup.find("img", attrs={"class": "coverart_img"}).get(
            "src"
        )
        save_image_to_file(cover_link, filename)

    except:
        print(f"Unable to download {album.name} cover")
        return 0
    return 1


def download_image_from_last(album):
    time.sleep(2 * random.random() + 1)  # do not download too fast
    url = "http://ws.audioscrobbler.com/2.0/"
    body = {
        "method": "album.getinfo",
        "api_key": LAST_API_KEY,
        "artist": album.artist,
        "album": album.name,
        "autocorrect": 1,
        "format": "json",
    }
    filename = album.id + ".jpg"

    r = requests.get(url, body)
    if r.status_code == 403:
        print(f"Unable to download {album.name} cover")
        return 0
    album_info = r.json()["album"]
    cover_link = album_info["image"][3]["#text"]
    save_image_to_file(cover_link, filename)
    return 1


def save_image_to_file(image_link, filename):
    image = requests.get(image_link, stream=True)
    if image.status_code == 200:
        with open(os.path.join(IMAGES_DIR, filename), "wb") as out_file:
            image.raw.decode_content = True
            shutil.copyfileobj(image.raw, out_file)
        ensure_size(filename)


def cached(album):
    return os.path.isfile(os.path.join(IMAGES_DIR, album.id))


def ensure_size(filename, size=(300, 300)):
    im = Image.open(os.path.join(IMAGES_DIR, filename))
    if im.size != size:
        im = im.resize(size)
        im.save(os.path.join(IMAGES_DIR, filename))
    im.close()
