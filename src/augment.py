import os
from image import *
from fast import *
from kaze import *


def search_all(image_path, db_path):
    """
    Search in the db for the best match
    """
    best_img = 0
    best_matches = 0
    best_path = 0
    image_test = open_image(image_path)
    for f in os.listdir(db_path):
        img_path = os.path.join(db_path, f)
        img = open_image(img_path)
        _, _, _, _, filtered_matches, _ = kaze_match_results(img, image_test)
        if len(filtered_matches) > best_matches:
            best_img = img
            best_matches = len(filtered_matches)
            best_path = img_path
    return best_img, best_path

