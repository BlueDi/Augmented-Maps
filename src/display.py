import cv2 as cv
import numpy as np


def show_match_result(image_base,  image_test, keypointsA, keypointsB, matches, homography=None):

    imgMatch = cv.drawMatches(image_base, keypointsA, image_test, keypointsB, matches, None)

    if homography is not None:
        h,w = image_base.shape[:2]
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts, homography)
        dst += np.float32([w,0])
        imgMatch = cv.polylines(imgMatch,[np.int32(dst)],True,(0,255,0),3, cv.LINE_AA)

    cv.namedWindow("matches", cv.WINDOW_KEEPRATIO)

    print("Showing matched results")
    cv.imshow("matches", imgMatch)

    print("Showing base image with augmented transformation")
    transform_with_homography(image_base, homography)

    print("Showing augmented image with base transformation")
    transform_with_inverse_homography(image_test, homography)


def transform_with_homography(image, homography):
    dsize = (image.shape[1], image.shape[0])
    new_image = cv.warpPerspective(image, homography, dsize)
    cv.imshow("Homographied image", new_image)

def transform_with_inverse_homography(image, homography):
    inverse = np.linalg.inv(homography)
    dsize = (image.shape[1], image.shape[0])
    new_image = cv.warpPerspective(image, inverse, dsize)
    cv.imshow("Homographied inverse image", new_image)


