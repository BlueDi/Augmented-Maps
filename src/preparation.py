import cv2 as cv
import os
from augment import *
from database import *


IMAGE_FOLDER = '../resources/images'


def click_map_callback(event, x, y, flags, param):
    """
    Callback for the image
    When left click the image, print the x and y
    """
    database = param
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
        database.update(feature_point)


def click_map(image, database, window_name="Preparation"):
    """
    Create the callback for the image
    Display the image
    """
    cv.namedWindow(window_name)
    cv.setMouseCallback(window_name, click_map_callback, database)

    cv.imshow(window_name, image)
    cv.waitKey(0)

