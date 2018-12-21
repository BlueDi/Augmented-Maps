import os
import database as db
import display as disp
import image as img
import kaze
import numpy as np
import utils
import cv2 as cv
import math
import sys


DB_FP = '../resources/feature_points.pkl'
DB_POI = '../resources/points_of_interest.pkl'
IMAGE_BASE = '../resources/db/porto_original.png'
IMAGE_TEST = '../resources/test/porto_rotate.jpg'

DEBUG = False


def applyAugmentedComponents(homography, image_base_display, image_base_test):
    points_of_interest = db.load_db(DB_POI)

    width, heigth = image_base_test.shape[:2]
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

    place_center(image_base_test, xCenter, yCenter)
    place_compass(image_base_test, xCenter, yCenter)
    place_closest_interest(image_base_test, closest_point)

    cv.imshow("Augmented", image_base_test)
    cv.waitKey(0)   


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



def get_kp(file_name):
    feature_points = db.load_db(DB_FP)

    if file_name in feature_points:
        kaze_features = feature_points[file_name]
        kp = utils.list_to_kp(kaze_features['kp_list'])
    else:
        raise Exception('Run preparation program first.')

    return kp, kaze_features['desc']


def main():

    if(len(sys.argv) > 1 and (sys.argv[1] == '--debug' or sys.argv[1] == '-d')):
        DEBUG = True
    else:
        DEBUG = False

    '''
    Initializing Augmentation
    '''
    if DEBUG: print("Loading Feature Points")
    kp, desc = get_kp(IMAGE_BASE)
    
    if DEBUG: print("Loading Images")
    image_base = img.open_image_for_process(IMAGE_BASE)
    image_test = img.open_image_for_process(IMAGE_TEST)
    image_base_display = img.open_image_for_display(IMAGE_BASE)
    image_test_display = img.open_image_for_display(IMAGE_TEST)

    if DEBUG: print("Matching Features with new image")
    filtered_matches, homography, kp2 = kaze.short_match_results(kp, desc, image_test)

    if DEBUG: 
        print("Displaying matching results")
        disp.show_match_result(image_base, kp, image_test, kp2, filtered_matches, homography)
    
    if DEBUG: print("Applying Augmented Components")
    applyAugmentedComponents(homography, image_base_display, image_test_display)

if __name__ == '__main__':
    main()

