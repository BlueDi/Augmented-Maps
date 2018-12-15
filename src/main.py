import cv2 as cv
import os, os.path
from display import *
from fast import *
from image import *
from kaze import *


IMAGE_FOLDER = '../resources/db'
IMAGE_TEST = '../resources/test/clerigos.png'
WINDOW_NAME = 'match'


def search_all():
    """
    Search in the db for the best match
    """
    best_img = 0
    best_matches = 0
    best_path = 0
    image_test = open_image(IMAGE_TEST)
    for f in os.listdir(IMAGE_FOLDER):
        img_path = os.path.join(IMAGE_FOLDER,f)
        img = open_image(img_path)
        _, _, _, _, filtered_matches, _ = kaze_match_results(img, image_test)
        if len(filtered_matches) > best_matches:
            best_img = img
            best_matches = len(filtered_matches)
            best_path = img_path
    return best_img, best_path


def click_map_callback(event, x, y, flags, param):
    """
    Callback for the image
    When left click the image, print the x and y
    """
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(param, (x,y), 100, (255,0,0), -1)
        print x, y


def click_map(image):
    """
    Create the callback for the image
    Display the image
    """
    cv.namedWindow(WINDOW_NAME)
    cv.setMouseCallback(WINDOW_NAME, click_map_callback, image)

    cv.imshow(WINDOW_NAME, image)
    cv.waitKey(0)


def main():
    img, path = search_all()
    click_map(img)


if __name__ == '__main__':
    main()

