import cv2 as cv
import os, os.path
from display import *
from fast import *
from image import *
from kaze import *


IMAGE_FOLDER = '../resources/db'
IMAGE_TEST = '../resources/test/clerigos.png'


def search_all():
    """
    Search in the db for the best match
    """
    best_img = 0
    best_matches = 0
    image_test = open_image(IMAGE_TEST)
    for f in os.listdir(IMAGE_FOLDER):
        img_path = os.path.join(IMAGE_FOLDER,f)
        img = open_image(img_path)
        _, _, _, _, filtered_matches, _ = kaze_match_results(img, image_test)
        if len(filtered_matches) > best_matches:
            best_img = img
            best_matches = len(filtered_matches)
    cv.imshow('best', best_img)
    cv.waitKey(0)


def main():    
    search_all()


if __name__ == '__main__':
    main()

