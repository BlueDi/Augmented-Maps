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

def applyHomography(homography, points_of_interest, image1, image2):

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


def augment(image1, image2, points_of_interest):
    kaze_kp1, _, kaze_kp2, _, filtered_matches, homography = kaze.match_results(image1, image2)
    applyHomography(homography, points_of_interest, image1, image2)
    disp.show_match_result(image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography)

def analyse(file_name, image_test, feature_points, best):
    """
    Analyses 2 images and compares with the best result
    If the image is stored on the db, it uses the values from the db
    Else calculates de kaze features and saves them to the db
    """
    img_path = os.path.join(DB_FOLDER, file_name)
    image = img.open_image(img_path)

    if file_name in feature_points:
        kaze_features = feature_points[file_name]
        kp = utils.list_to_kp(kaze_features['kp_list'])
        filtered_matches, _ = kaze.short_match_results(kp, kaze_features['desc'], image_test)
    else:
        kp, desc, _, _, filtered_matches, _ = kaze.match_results(image, image_test)
        feature_point =	{
            file_name: {
                'path': img_path,
                'kp_list': utils.kp_to_list(kp),
                'desc': desc
            }
        }
        feature_points.update(feature_point)

    if len(filtered_matches) > best['matches']:
        best['img'] = image
        best['matches'] = len(filtered_matches)
        best['path'] = img_path
    return best, feature_points

def search_all(image_path, db_path, points_of_interest, display=False):
    """
    Search in the db for the best match
    """
    best = {
        'img': 0,
        'matches': 0,
        'path': 0
    }
    image_test = img.open_image(image_path)

    feature_points = db.load_db(db_path)

    print 'Calculating feature points'
    for f in os.listdir(DB_FOLDER):
        best, feature_points = analyse(f, image_test, feature_points, best)
    print 'Finished calculating feature points'

    if display:
        augment(best['img'], image_test, points_of_interest)

    db.save_db(db_path, feature_points)
    return best['img'], best['path']

