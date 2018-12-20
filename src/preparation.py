import cv2 as cv
import os
import database as db
import image as img
import utils


DB_FOLDER = '../resources/db'
DB_FP = '../resources/feature_points.pkl'
IMAGE_BASE = 'porto_mapa.png'
IMAGE_FOLDER = '../resources/images'


def set_feature_point(file_name, db_path):
    """
    Analyses 2 images and compares with the best result
    If the image is stored on the db, it uses the values from the db
    Else calculates de kaze features and saves them to the db
    """
    image = img.open_image(file_name)
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


def click_map_callback(event, x, y, flags, database):
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
        database.update(point_of_interest)


def click_map(database, image_base, window_name="Preparation"):
    """
    Create the callback for the image
    Display the image
    """
    map_image = img.open_image(image_base)
    cv.namedWindow(window_name)
    cv.setMouseCallback(window_name, click_map_callback, database)

    cv.imshow(window_name, map_image)


def main():
    DB_POI = '../resources/points_of_interest.pkl'
    IMAGE_BASE = '../resources/db/porto_mapa.png'

    points_of_interest = db.load_db(DB_POI)
    click_map(points_of_interest, IMAGE_BASE, window_name="Preparation")
    db.save_db(DB_POI, points_of_interest)
    set_feature_point(IMAGE_BASE, DB_FP)


if __name__ == '__main__':
    main()

