"""
DESCRIPTION
    This script is designed to create collages of albums
    based on user rating criteria

FUNCTIONS
    collage(username, *stars)
        Return image of random albums

USAGE
    python build_collage.py User -s 4.0 4.5 5.0
    python build_collage.py User -s 5.0
"""

from .make_collage import make_collage
from .scraping import get_raw_data, get_images


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("username",
                        help="you can find your username after ~ sign:\
                        https://rateyourmusic.com/~User")
    parser.add_argument("stars",
                        nargs='+',
                        help="stars to pick covers from")
    parser.add_argument("filename",
                        help="File will be saved in the project directory\n\
                        example: my_collage")
    parser.add_argument("-r", dest="rows", default=4,
                        help="Number of rows\n\
                        example: -r 5 (default number is 4"")
    parser.add_argument("-c", dest="cols", default=4,
                        help="Number of collumns\n\
                        example: -c 5 (default number is 4")
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    username = args.username
    stars = args.stars
    output = args.filename
    try:
         n_rows, n_cols = map(int, [args.rows, args.cols])
     except ValueError as e:
         print(e)
         print("Number of rows/columns is invalid")
         return

    raw_data = get_raw_data(username, stars)
    pics = get_images(raw_data, n_rows*n_cols)
    if pics:
        make_collage(pics, output, n_rows, n_cols)
    else:
        print("No albums with that rating(s)")
