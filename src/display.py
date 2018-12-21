import cv2 as cv
import numpy as np

CIRCLE_SIZE = 7

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

def place_center(image, x, y):
    cv.circle(image, (x,y), 7, (19, 255, 255), -1)
    cv.circle(image, (x,y), 7, (0,0,0), 1)
    pass


def place_compass(image, x, y):
    pass

'''
    point = {
        'name': None,
        'distance': 99999,
        'x': 0,
        'y': 0,
        'originX': 0,
        'originY': 0
    }
'''
def place_intereset_point(image, point):
    if(point['name'] is not None): #Green
        cv.circle(image, (point['x'], point['y']), CIRCLE_SIZE, (19, 124, 17), -1)
        cv.circle(image, (point['x'], point['y']), CIRCLE_SIZE, (0,0,0), 1)
        place_label(point['x'], point['y'], point['name'], image)
    return image

def place_label(xCenter, yCenter, label, image):
    size = cv.getTextSize(label, cv.FONT_HERSHEY_PLAIN, 1, 2)
    w = size[0][0]
    x = xCenter - int(round(w/2.0))
    y = yCenter - int(round(CIRCLE_SIZE/2.0)) - 4
    cv.putText(image, label, (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2)



