import cv2 as cv
from display import *
from fast import *
from image import *
from kaze import *


def main():
    #Open image
    image_name1 = '../resources/poster1.jpg'
    image_name2 = '../resources/poster2.jpg'
    image1 = openImage(image_name1)
    image2 = openImage(image_name2)
    cv.imshow('image', image1)

    #1. Extracting local features
    fast_get_features(image1)
    kaze_get_features(image1)

    #2. Matching local features
    image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography = kaze_match_results(image1, image2)
    show_match_result(image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography)

    cv.waitKey(0)


if __name__ == '__main__':
    main()

