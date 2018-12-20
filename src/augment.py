import os
import database as db
import display as disp
import image as img
import kaze
import numpy as np
import utils
import cv2 as cv
import math


DB_FOLDER = '../resources/db'
DB_FP = '../resources/feature_points.pkl'
DB_POI = '../resources/points_of_interest.pkl'
IMAGE_BASE = '../resources/db/porto_mapa.png'
IMAGE_TEST = '../resources/test/boavista.png'


def applyHomography(homography, image1, image2):
    points_of_interest = db.load_db(DB_POI)

    width, heigth = image2.shape
    xCenter = int(round(heigth/2.0))
    yCenter = int(round(width/2.0))
    closest_point = {
        'name': None,
        'distance': 99999,
        'x': 0,
        'y': 0,
        'originX': 0,
        'originY': 0
    }
    
    for name, point in points_of_interest.items():
        origin = np.array([[point['x']], [point['y']], [1]])
        points = np.matmul(homography, origin)
        pX = int(round(points[0]/points[2]))
        pY = int(round(points[1]/points[2]))
        dist = math.hypot(xCenter - pX, yCenter - pY)
        if(dist < closest_point['distance'] and pX >= 0 and pX < width and pY >= 0 and pY < heigth):
            closest_point['name'] = name
            closest_point['distance'] = dist
            closest_point['x'] = pX
            closest_point['y'] = pY
            closest_point['originX'] = point['x']
            closest_point['originY'] = point['y']

    backtorgb = cv.cvtColor(image2,cv.COLOR_GRAY2RGB)

    place_center(backtorgb, xCenter, yCenter)
    place_compass(backtorgb, xCenter, yCenter)
    place_closest_interest(backtorgb, closest_point)

    cv.imshow("Augmented", backtorgb)   


def place_center(image, x, y):
    cv.circle(image, (x,y), 7, (19, 255, 255), -1)
    cv.circle(image, (x,y), 7, (0,0,0), 1)
    pass


def place_compass(image, x, y):
    pass


def place_closest_interest(image, closest_point):
    if(closest_point['name'] is not None): #Green
        cv.circle(image, (closest_point['x'], closest_point['y']), 7, (19, 124, 17), -1)
        cv.circle(image, (closest_point['x'], closest_point['y']), 7, (0,0,0), 1)


def augment(image1, kp1, desc1, image2):
    filtered_matches, homography, kp2 = kaze.short_match_results(kp1, desc1, image2)
    applyHomography(homography, image1, image2)
    disp.show_match_result(image1, kp1, image2, kp2, filtered_matches, homography)


def get_kp(file_name):
    feature_points = db.load_db(DB_FP)

    if file_name in feature_points:
        kaze_features = feature_points[file_name]
        kp = utils.list_to_kp(kaze_features['kp_list'])
    else:
        raise Exception('Run preparation first.')

    return kp, kaze_features['desc']


def compare(image1, image2):
    kaze_kp1, _, kaze_kp2, _, filtered_matches, homography = kaze.match_results(image1, image2)
    disp.show_match_result(image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography)


def main():
    kp, desc = get_kp(IMAGE_BASE)
    
    image_base = img.open_image(IMAGE_BASE)
    image_test = img.open_image(IMAGE_TEST)

    augment(image_base, kp, desc, image_test)


if __name__ == '__main__':
    main()

