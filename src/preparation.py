import argparse
import cv2 as cv
import os
import database as db
import image as img
import utils
import sys
import display as disp


DB_POI = '../resources/points_of_interest.pkl'
DB_FP = '../resources/feature_points.pkl'
IMAGE_FOLDER = '../resources/images'
IMAGE_BASE = '../resources/db/porto_original.png'

DEBUG = False

def calculate_feature_points(file_name, db_path):
    """
    Analyzes 2 images and compares with the best result
    If the image is stored on the db, it uses the values from the db
    Else calculates de kaze features and saves them to the db
    """
    image = img.open_image_for_process(file_name)
    feature_points = db.load_db(db_path)

    if file_name in feature_points:
        kaze_features = feature_points[file_name]
        kp = utils.list_to_kp(kaze_features['kp_list'])
    else:
        detector = cv.KAZE_create()
        matcher = cv.FlannBasedMatcher()
        kp, desc = detector.detectAndCompute(image, None)

        feature_point =	{
            file_name: {
                'path': file_name,
                'kp_list': utils.kp_to_list(kp),
                'desc': desc
            }
        }
        feature_points.update(feature_point)
        db.save_db(db_path, feature_points)

    best = {}
    best['img'] = image
    best['path'] = file_name

    return best


def click_map_callback(event, x, y, flags, param):
    """
    Callback for the image
    When left click the image, print the x and y
    """
    if event == cv.EVENT_LBUTTONDOWN:
        print 'Coords:', x, y
        image_name = raw_input('Image name: ')
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        print 'Path:', image_path
        point_of_interest =	{
            image_name: {
                'path': image_path,
                'x': x,
                'y': y
            }
        }
        param['db'].update(point_of_interest)

        point = {
            'name': image_name,
            'x': x,
            'y': y
        }
        disp.place_intereset_point(param['img'], point)
        cv.imshow(param['window'],param['img'])




def click_map(database, image_base, window_name="Preparation"):
    """
    Create the callback for the image
    Display the image
    """
    if DEBUG: print("Loading image")
    map_image = img.open_image_for_display(image_base)
    cv.namedWindow(window_name)

    if DEBUG: print("Displaying existing points")
    for name, point in database.items():
        point = {'name': name, 'x': point['x'], 'y': point['y']}
        disp.place_intereset_point(map_image, point)

    if DEBUG: print("Creating callback")
    param = {'db': database, 'img': map_image, 'window': window_name}
    cv.setMouseCallback(window_name, click_map_callback, param)

    if DEBUG: print("Displaying image")
    cv.imshow(window_name, map_image)
    cv.waitKey(0)


def parse_arguments():
    '''Checks for flags'''
    parser = argparse.ArgumentParser(description="Prepare the map image")
    parser.add_argument('-d','--debug', action='store_true', help='Debug Mode')
    args = parser.parse_args()
    global DEBUG
    DEBUG = args.debug


def main():
    '''Initializing Preparation'''
    parse_arguments()

    if DEBUG: print("Loading Points of interest databse")
    points_of_interest = db.load_db(DB_POI)
    
    if DEBUG: print("Waiting for Points of interest")
    click_map(points_of_interest, IMAGE_BASE, window_name="Preparation")

    if DEBUG: print("Saving Points of Interest")
    db.save_db(DB_POI, points_of_interest)

    if DEBUG: print("Calculating Feature Points")
    calculate_feature_points(IMAGE_BASE, DB_FP)

    if DEBUG: print("Successful, exiting Preparation")

if __name__ == '__main__':
    main()

