import os
import display as disp
import image as img
import kaze


def compare(image1, image2):
    image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography = kaze.match_results(image1, image2)
    disp.show_match_result(image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography)


def search_all(image_path, db_path, display=False):
    """
    Search in the db for the best match
    """
    best_img = 0
    best_matches = 0
    best_path = 0
    image_test = img.open_image(image_path)
    for f in os.listdir(db_path):
        img_path = os.path.join(db_path, f)
        image = img.open_image(img_path)
        _, _, _, _, filtered_matches, _ = kaze.match_results(image, image_test)
        if len(filtered_matches) > best_matches:
            best_img = image
            best_matches = len(filtered_matches)
            best_path = img_path

    if display:
        compare(best_img, image_test)

    return best_img, best_path

