# -*- coding: utf-8 -*-
"""
Поиск пользователей с заданной оценкой по заданному альбому на rateyourmusic.com

Usage: python user_search <URL> [stars condition]


Use case:
    python user_search https://rateyourmusic.com/release/album/holy-balm/activity/ --stars 5 —— finds all users who rated this album exactly 5 stars
    python user_serach https://rateyourmusic.com/release/album/diiv/is-the-is-are/ -s 4-5    —— finds all user who rated this album 4 stars or higher
"""


import sys
from selenium import webdriver
import bs4
import argparse
from time import sleep
import random

HOME = "https://rateyourmusic.com"
GECKO = r'C:\\driver.exe'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("album_link",
                        help="use RYM link for example: https://rateyourmusic.com/release/album/diiv/is-the-is-are/")
    parser.add_argument("-s", "--stars",
                        help="use inequality symobls or pick exact number of stars")
    return parser


def parse_input_stars(data) -> (float, float):
    # returns search range
    try:
        s = data.split('-')
        stars_lower_bound = float(s[0])
        stars_upper_bound = float(s[-1])
    except (AttributeError, ValueError, TypeError):
        print("InputError: incorrect format, use -h or --help to get more information")
        sys.exit(0)

    return (stars_lower_bound, stars_upper_bound)


def parse_rym_html(html):
    # returns list of (user, rating) from "rating_section"
    data = []
    soup = bs4.BeautifulSoup(html)
    for stuff in soup.find_all("div", {"class": "catalog_header"}):

        # apparently "usero"- online; "user" - offline
        if stuff.find("a", {"class": "user"}):
            user = HOME + stuff.find("a", {"class": "user"}).get('href')
        elif stuff.find("a", {"class": "usero"}):
            user = HOME + stuff.find("a", {"class": "usero"}).get('href')
        else:
            user = ''
        title = (stuff.find("img").get("title"))
        rating = float(title[:4])
        data.append((user, rating))
    return data


def get_content_from_page(html, stars_lower_bound, stars_upper_bound):
    # returns list of users who satisfies the specified criteria
    content = []
    data = parse_rym_html(html)
    for user, rating in data:
        if rating >= stars_lower_bound and rating <= stars_upper_bound:
            content.append(user)
    return content


def get_content(album_link, stars_lower_bound, stars_upper_bound) -> [str]:
    content = []
    browser = webdriver.(executable_path=)
    browser.get(album_link)
    ratings = browser.find_element_by_class_name("catalog_section")  # section with ratings
    html = browser.page_source
    content += get_content_from_page(html, stars_lower_bound, stars_upper_bound)

    pages = True
    try:
        ratings.find_element_by_class_name("navlinknum")
    except:
        pages = False
    if pages:  # means that there is more than one page
        elems = ratings.find_elements_by_class_name("navlinknum")
        last_page = int(elems[-1].text)

        # iterate over all pages in rating_section starting with second; first is already parsed
        # as sooon as we click on the next page and get content, we need to get new list of pages
        # have to wait a bit here to dodge the ban (:
        for page_num in range(2, last_page+1):
            elems = ratings.find_elements_by_class_name("navlinknum")
            for el in elems:
                curr_page = int(el.text)
                if curr_page == page_num:
                    el.click()
                    html = browser.page_source
                    content += get_content_from_page(html, stars_lower_bound, stars_upper_bound)
                    break
            sleep(2+2*random.random())
    return content


if __name__ == '__main__':
    args = get_parser().parse_args()
    album_link = args.album_link
    stars_lower_bound, stars_upper_bound = parse_input_stars(args.stars)
    content = get_content(album_link, stars_lower_bound, stars_upper_bound)
    if len(content) == 0:
        print("Query reports no result. \nTry other parameters or use -h flag to get help")
        sys.exit(0)

    album = album_link.split('/')
    album_band = album[-3]
    album_album = album[-2]
    with open("output_" + album_band + '_' + album_album + ".txt", 'w') as f:
        f.write(album_link + '\n')
        f.write("Criteria: " + args.stars + '\n'*3)
        f.write('\n'.join(content))
