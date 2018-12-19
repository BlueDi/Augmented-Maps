import cv2 as cv
import numpy as np


def show_match_result(imgA, keypointsA, imgB, keypointsB, matches, homography=None):
    imgMatch = cv.drawMatches(imgA, keypointsA, imgB, keypointsB, matches, None)

    if homography is not None:
        h,w = imgA.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts, homography)
        dst += np.float32([w,0])
        imgMatch = cv.polylines(imgMatch,[np.int32(dst)],True,(0,255,0),3, cv.LINE_AA)

    cv.namedWindow("matches", cv.WINDOW_KEEPRATIO)
    cv.imshow("matches", imgMatch)
    transform_with_homography(imgB, homography)
    cv.waitKey(0)


def transform_with_homography(image, homography):
    dsize = (image.shape[1], image.shape[0])
    new_image = cv.warpPerspective(image, homography, dsize)
    cv.imshow("Homographied image", new_image)