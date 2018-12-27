import argparse
import os
import database as db
import display as disp
import image as img
import pyramid as pyr
import kaze
import numpy as np
import utils
import cv2 as cv
import math
import sys
import utils

DB_FP = '../resources/feature_points.pkl'
DB_POI = '../resources/points_of_interest.pkl'
IMAGE_BASE = '../resources/db/porto_original.png'
IMAGE_TEST = '../resources/test/porto_rotate.jpg'
IMAGE_FOLDER = '../resources/images'

DEBUG = False

#SCALE cada 57 pixeis sao 290 metros

def applyAugmentedComponents(homography, image_base_display, image_test_display):
    
    if DEBUG: print("Loading Points of Interest from Database")
    points_of_interest = db.load_db(DB_POI)

    if DEBUG: print("Calculating inverse homography")
    inverse = np.linalg.inv(homography)

    if DEBUG: print("Calculating important")
    heigth, width = image_test_display.shape[:2]
    xCenter = int(round(width/2.0))
    yCenter = int(round(heigth/2.0))

    if DEBUG: print("Placing center")
    disp.place_center(image_test_display, xCenter, yCenter)

    if DEBUG: print("Mapping center to original image")
    xOriginal, yOriginal = utils.map_coordinates(inverse, xCenter, yCenter)

    closest_point = {
        'name': None,
        'distance': 9999,
        'x': 0,
        'y': 0,
        'originX': 0,
        'originY': 0
    }
    
    if DEBUG: print("Finding closest interest point")
    for name, point in points_of_interest.items():
        dist = utils.calculate_distance(xOriginal, yOriginal, point['x'], point['y'])
        pX, pY = utils.map_coordinates(homography, point['x'], point['y'])

        print(dist, pX, pY, name, width, heigth)

        if(dist < closest_point['distance'] and pX >= 0 and pX < width and pY >= 0 and pY < heigth):
            closest_point['name'] = name
            closest_point['distance'] = dist
            closest_point['x'] = pX
            closest_point['y'] = pY
            closest_point['originX'] = point['x']
            closest_point['originY'] = point['y']

    if DEBUG: print("Calculationg real distance")
    if(closest_point['name'] is not None):
        distance_km = 290 * closest_point['distance'] / 57

    if DEBUG: print("Placing closest point")
    if(closest_point['name'] is not None):
        # Temporary, until it works. Then, x and y of the interest place point will be sent
        pyr.calculate_pyramid(homography, image_base_display, image_test_display, closest_point['x'], closest_point['y'])
        disp.place_intereset_point(image_test_display, closest_point, distance_km)

    if DEBUG: print("Placing compass")
    disp.place_compass(inverse, image_test_display, xCenter, yCenter, closest_point['x'], closest_point['y'])

    if DEBUG: print("Getting images of point")
    if(closest_point['name'] is not None):
        disp.create_slideshow(closest_point['name'], distance_km, IMAGE_FOLDER)
    
    cv.imshow("Augmented", image_test_display)
    cv.waitKey(0)   


def get_kp(file_name):
    feature_points = db.load_db(DB_FP)

    if file_name in feature_points:
        kaze_features = feature_points[file_name]
        kp = utils.list_to_kp(kaze_features['kp_list'])
    else:
        raise Exception('Run preparation program first.')

    return kp, kaze_features['desc']


def parse_arguments():
    '''Checks for flags'''
    global DEBUG
    global IMAGE_BASE
    global IMAGE_TEST
    parser = argparse.ArgumentParser(description="Augment the map image")
    parser.add_argument('-d', '--debug', action='store_true', help='Debug Mode')
    parser.add_argument('-ib', '--imagebase', default=IMAGE_BASE, help='Path to the frontal image of the map')
    parser.add_argument('-it', '--imagetest', default=IMAGE_TEST, help='Path to the image to be augmented')
    args = parser.parse_args()
    DEBUG = args.debug
    IMAGE_BASE = args.imagebase
    IMAGE_TEST = args.imagetest


def main():

    '''Initializing Augmentation'''
    parse_arguments()

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
        disp.show_match_result(image_base_display, image_test_display, kp, kp2, filtered_matches, homography)
    
    if DEBUG: print("Applying Augmented Components")
    applyAugmentedComponents(homography, image_base_display, image_test_display)

    if DEBUG: print("Successful, exiting Augment")

if __name__ == '__main__':
    main()

