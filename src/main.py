import cv2 as cv
import os
import augment as aug
import database as db
import preparation as prep


DB_FP = '../resources/feature_points.pkl'
DB_POI = '../resources/points_of_interest.pkl'
IMAGE_TEST = '../resources/test/boavista.png'
IMAGE_BASE = '../resources/db/porto_mapa.png'
WINDOW_NAME = 'match'


def main():
    points_of_interest = db.load_db(DB_POI)
    prep.click_map(points_of_interest, IMAGE_BASE, window_name="Preparation")
    img, path = aug.search_all(IMAGE_TEST, DB_FP, points_of_interest, True)
    db.save_db(DB_POI, points_of_interest)


if __name__ == '__main__':
    main()

