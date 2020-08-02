import os

# os files
DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(DIR, "images")

# rateyourmusic
RYM_URL = "https://rateyourmusic.com/"
ALBUMS_PER_PAGE = 25
HTTP_headers = {
    "Host": "rateyourmusic.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Upgrade-Insecure-Requests": "1",
}

# Last.fm
LAST_API_KEY = "64e9fa5a62db2ef067e27d46d6bb5ef3"

# postgres
db_config = {
    "database": "MY_BASE",
    "user": "postgres",
    "password": "Vincent1984Vfrbynji",
}
