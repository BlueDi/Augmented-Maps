import cv2 as cv
import os
import augment as aug
import database as db
import preparation as prep


DB_FP = '../resources/feature_points.pkl'
DB_POI = '../resources/points_of_interest.pkl'
IMAGE_TEST = '../resources/test/clerigos.png'
WINDOW_NAME = 'match'


def main():
    points_of_interest = db.load_db(DB_POI)
    prep.click_map(points_of_interest, WINDOW_NAME)
    img, path = aug.search_all(IMAGE_TEST, DB_FP, True)
    db.save_db(DB_POI, points_of_interest)

if __name__ == '__main__':
    main()

