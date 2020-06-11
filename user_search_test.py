# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 02:04:46 2019

@author: maks2
"""

from user_search import *

if __name__ == '__main__':
    
    #album_link = 'https://rateyourmusic.com/release/album/diiv/is-the-is-are/'
    #eq = '>='
    #stars = '5'
    
    args = get_parser().parse_args()
    print(args)
    album_link = args.album_link
    stars_lower_bound, stars_upper_bound = parse_input_stars(args.stars)
    print(album_link, stars_lower_bound, stars_upper_bound, sep='\n')