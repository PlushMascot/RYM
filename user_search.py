# -*- coding: utf-8 -*-
"""
Поиск пользователей по заданному альбому на rateyourmusic.com

Usage: python user_search <URL> [stars condition]


Example: 
    python user_search https://rateyourmusic.com/release/album/holy-balm/activity/ --stars 5 —— finds all users who rated this album exactly 5 stars
    python user_serach https://rateyourmusic.com/release/album/diiv/is-the-is-are/ -s >=4    —— finds all user who rated this album 4 stars or higher
"""

## ЕСЛИ АУТПУТ ПУСТОЙ, ТО ПОСОВЕТОВАТЬ ДРУГИЕ ПАРАМЕТРЫ ПОИСКА OR USE -HELP

import sys
import requests
import bs4
import argparse
import re

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("album_link", 
                        help="use RYM link for example: https://rateyourmusic.com/release/album/diiv/is-the-is-are/")
    parser.add_argument("-s", "--stars",
                        help="use inequality symobls or pick exact number of stars")
    return parser
    

def parse_stars(data) ->(str, float) :
    try:
        eq = re.search(r'[^\d.]+', data).group()
    except (AttributeError, ValueError, TypeError):
        eq = '='
    
    try:
        star = float(re.search(r'[\d.]+', data).group())
    except (AttributeError, ValueError, TypeError):
        print("incorrect format, use -h or --help to get more information")
        sys.exit(0)
        
    return eq, star


def get_content(album_link, eq, star) ->List[str]:
    content = []
    
    lower_bound = 0.5
    upper_bound = 5
    while True:
        ...
        
        if s >= lower_bound and s <= upper_bound:
    content.append(link)
    return content


if __name__ == '__main__':
    args = get_parser().parse_args()
    album_link = args.album_link
    eq, star = parse_stars(args.stars)
    content = get_content(album_link, eq, star)
    print('\n'.join(content))
    
    
    
    
    