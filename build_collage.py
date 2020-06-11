"""
DESCRIPTION
    This script is designed to create collages of albums
    based on user rating criteria

FUNCTIONS
    collage(username, *stars, image_format)
        Return image of random albums

USAGE
    python build_collage.py User -s 4.0 4.5 5.0 -f .jpg
    python build_collage.py User -s 5.0            (default is .png)
"""

import argparse
import bs4
import selenium


RYM = "https://rateyourmusic.com/~"


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("username",
                        help="you can find your username after ~ sign:\
                        https://rateyourmusic.com/~User")
    parser.add_argument("-s",
                        nargs='+',
                        help="stars to pick covers from")
    parser.add_argument("image_format")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    username = args.username
    *stars = parse_input_stars(args.stars)
    image_format = args.image_format
    collage(username, stars, image_format)