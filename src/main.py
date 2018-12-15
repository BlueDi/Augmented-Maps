import cv2 as cv
import os
from augment import *
from database import *
from display import *
from preparation import *


DB_FOLDER = '../resources/db'
DB_NAME = '../resources/feature_points.dat'
IMAGE_TEST = '../resources/test/clerigos.png'
WINDOW_NAME = 'match'


def main():
    feature_points = load_db(DB_NAME)
    img, path = search_all(IMAGE_TEST, DB_FOLDER)
    click_map(img, feature_points, WINDOW_NAME)
    save_db(DB_NAME, feature_points)

if __name__ == '__main__':
    main()

