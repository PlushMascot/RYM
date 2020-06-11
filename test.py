from build_collage import get_parser

if __name__ == '__main__':
    args = get_parser().parse_args()
    username = args.username
    stars = args.stars
    print(stars)
