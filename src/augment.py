import os
import database as db
import display as disp
import image as img
import kaze
import utils


DB_FOLDER = '../resources/db'


def compare(image1, image2):
    kaze_kp1, _, kaze_kp2, _, filtered_matches, homography = kaze.match_results(image1, image2)
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

def search_all(image_path, db_path, display=False):
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

    for f in os.listdir(DB_FOLDER):
        best, feature_points = analyse(f, image_test, feature_points, best)

    if display:
        compare(best['img'], image_test)

    db.save_db(db_path, feature_points)
    return best['img'], best['path']

