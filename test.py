from scraping import *


RYM_URL = "https://rateyourmusic.com/"
username = "sharifi"
stars = ["2.5", "3.0"]
pages_to_scan = 2
collection_url = (
    f"{RYM_URL}/collection/{username}/"
    f"d.rp,a,l,aat,r{min(stars)}-{max(stars)},n{25}/")


albums_data = []
print(collection_url)
for page in range(pages_to_scan):
    albums_data.extend(get_content(collection_url + f"{page}"))
