import argparse
import bs4
import requests
import json
import os
import time
import shutil
import random
#import pdb

from typing import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from my_logger import exception_log


DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(DIR, "images")
RYM_URL = "https://rateyourmusic.com/"
ALBUMS_PER_PAGE = 25
GECKODRIVER = r'C:\gecko\geckodriver.exe'


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class WebDriver(metaclass=SingletonMeta):
    def __init__(self):
        options = Options()
        options.add_argument('-headless')
        self.driver = Firefox(executable_path=GECKODRIVER, options=options)


def get_raw_data(username: str, stars: List[float]) -> List[Any]:
    """
    Return list of {username}s albums within the range of {stars}
    """

    collection_url = (
        f"{RYM_URL}/collection/{username}/"
        f"d.rp,a,l,aat,r{min(stars)}-{max(stars)},n{ALBUMS_PER_PAGE}/")

    user_url = RYM_URL + f"~{username}"
    albums_to_scan = analyze_musicrating(user_url, stars)
    if albums_to_scan == 0:
        return []

    pages_to_scan = albums_to_scan // ALBUMS_PER_PAGE + 1
    albums_data = []
    for page in range(1, pages_to_scan + 1):
        albums_data.extend(get_content(collection_url + f"{page}"))

    return albums_data


def analyze_musicrating(user_url: str, stars: List[str]) -> Any:
    """
    Counts how many albums in total user had rated within the range of {stars}.
    """

    driver = WebDriver().driver
    driver.get(user_url)
    html_source = driver.page_source
    soup = bs4.BeautifulSoup(html_source, features="html.parser")
    table_div = soup.find('div', {'id': 'musicrating'})
    table = table_div.find('table', attrs={'class': 'mbgen'})

    number_of_reviews = []
    for row in table.find_all('tr'):
        column = row.find('b') # number of reviews with rating [5.0 ... 0.5]
        if column:
            number_of_reviews.append(column.text)

    albums_to_scan = 0
    for star, i in zip(range(50, -5, -5), range(11)):
        # due to implentation detail - user 'stars' input stored in List[str]
        star = str(0.1*star)
        if star in stars:
            albums_to_scan += int(number_of_reviews[i].replace(',', ''))
    return albums_to_scan


def get_content(link: str):
    """
    explanation of url params:
    https://rateyourmusic.com/wiki/Sandbox:Links

    response example:
        [
        {
         'artist': 'The Beatles'
         'album_name': 'Yellow Submarine Songtrack',
         'album_link': '/release/comp/the-beatles/yellow-submarine-songtrack/',
         'id': 'Album261'
        }
        ]
    """
    response = []
    driver = WebDriver().driver
    driver.get(link)
    html_source = driver.page_source
    soup = bs4.BeautifulSoup(html_source, features="html.parser")
    table = soup.find('table', attrs={'class': 'mbgen'})
    table_header = True
    for row in table.find_all('tr'):
        if not table_header:
            artist = row.find('a', attrs={'class': 'artist'}).text
            album = row.find('a', attrs={'class': 'album'}).text
            relative_album_link = row.find('a', attrs={'class': 'album'}).get('href')
            cover = row.find('a', attrs={'class': 'album'}).get('title')
            response.append(
                {
                 'artist': artist,
                 'album_name': album,
                 'album_link': RYM_URL.rstrip('/') + relative_album_link,
                 'id': cover[1:-1],
                 }
            )
        table_header = False
    return response


def get_images(albums_data, n: int):
    """
    downloads images if there is no aldready
    randomly picks n images out of {len(album_data)}
    returns list of id's
    """
    pics = []
    for album in albums_data:
        if not os.path.isfile(os.path.join(IMAGES_DIR, album['id'])):
            time.sleep(2*random.random()+1)
            try:
                download(album['album_link'], album["id"])
            except:
                print(f"Unable to download {album["album_name"]} cover")
                continue
        pics.append(album["id"])
    return random.sample(pics, n)


@exception_log
def download(album_link, filename):
    driver = WebDriver().driver
    driver.get(album_link)
    html_source = driver.page_source
    soup = bs4.BeautifulSoup(html_source, features="html.parser")
    cover_link = 'https:' + soup.find('img', attrs={'class': 'coverart_img'}).get('src')
    response = requests.get(cover_link, stream=True)
    if response.status_code == 200:
        save_image_to_file(response, filename)


def save_image_to_file(image, filename):
    with open(os.path.join(IMAGES_DIR, filename + ".jpg"), 'wb') as out_file:
        image.raw.decode_content = True
        shutil.copyfileobj(image.raw, out_file)
