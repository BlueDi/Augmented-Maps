import cv2 as cv
import os
from augment import *
from database import *
from display import *


DB_FOLDER = '../resources/db'
DB_NAME = '../resources/feature_points.dat'
IMAGE_FOLDER = '../resources/images'
IMAGE_TEST = '../resources/test/clerigos.png'
WINDOW_NAME = 'match'
feature_points = {}


def click_map_callback(event, x, y, flags, param):
    """
    Callback for the image
    When left click the image, print the x and y
    """
    global feature_points
    if event == cv.EVENT_LBUTTONDOWN:
        print 'Coords:', x, y
        image_name = raw_input('Image name: ')
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        print 'Path:', image_path
        feature_point =	{
            image_name: {
                'path': image_path,
                'x': x,
                'y': y
            }
        }
        feature_points.update(feature_point)


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
    global feature_points
    feature_points = load_db(DB_NAME)
    img, path = search_all(IMAGE_TEST, DB_FOLDER)
    click_map(img)
    save_db(DB_NAME, feature_points)


if __name__ == '__main__':
    main()

