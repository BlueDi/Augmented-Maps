import cv2 as cv
import numpy as np

line_color = (0, 0, 0)
line_thickness = 2
line_size = 25
fill_color = (0, 255, 0)


def draw_pyramid():

    img = cv.imread("../resources/db/porto_mapa.png")
    img2 = cv.imread("../resources/db/porto_mapa_x.png")
    draw(img)

    # Find the rotation and translation vectors.
    #ret, rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
    # project 3D points to image plane
    #imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)

    #rotV, _ = cv.Rodrigues([1,0,0])
    #points = np.float32([[100, 0, 0], [0, 100, 0], [0, 0, 100], [0, 0, 0]]).reshape(-1, 3)
    #axisPoints, _ = cv.projectPoints(points, rotV, t, K, (0, 0, 0, 0))

    cv.imshow("pyramid", img)
    cv.waitKey(0)
    return img


def draw(img):
    height, width, channels = img.shape
    center, corner_up_left, corner_up_right, corner_bottom_left, corner_bottom_right = get_corners(width, height)

    # fill the whole polygon with fill_color
    corners = np.array([corner_up_left, corner_up_right, corner_bottom_right, corner_bottom_left])
    cv.fillPoly(img, pts=[corners], color=fill_color)

    # draw all lines from the center to the corners
    cv.line(img, tuple(center), tuple(corner_up_left), line_color, line_thickness)
    cv.line(img, tuple(center), tuple(corner_up_right), line_color, line_thickness)
    cv.line(img, tuple(center), tuple(corner_bottom_left), line_color, line_thickness)
    cv.line(img, tuple(center), tuple(corner_bottom_right), line_color, line_thickness)

    # connect all corners
    cv.line(img, tuple(corner_up_left), tuple(corner_up_right), line_color, line_thickness)
    cv.line(img, tuple(corner_up_right), tuple(corner_bottom_right), line_color, line_thickness)
    cv.line(img, tuple(corner_bottom_right), tuple(corner_bottom_left), line_color, line_thickness)
    cv.line(img, tuple(corner_bottom_left), tuple(corner_up_left), line_color, line_thickness)

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    corners = np.array([center, corner_up_left, corner_up_right, corner_bottom_right, corner_bottom_left], np.float32)
    objp = np.zeros((5, 3), np.float32)
    objp[0] = [0, 0, 0]
    objp[1] = [-1, -1, 0]
    objp[2] = [-1, 1, 0]
    objp[3] = [1, 1, 0]
    objp[4] = [1, -1, 0]

    objpoints = []
    imgpoints = []
    # cv.cornerSubPix(img, corners, (11, 11), (-1, -1), criteria)
    imgpoints.append(corners)

    objpoints.append(objp)
    #objp1 = [0,0,1]
    #objpoints.append(objp1)


    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (img.shape[1], img.shape[0]), None, None)
    ret, rvecs, tvecs = cv.solvePnP(objp, corners, mtx, dist)
    #imgpts, jac = cv.projectPoints(corners, rvecs, tvecs, mtx, dist)
    print(mtx)
    print(rvecs)


def get_corners(width, height):
    center = [width/2, height/2]
    corner_up_left = [width/2 - line_size/2, height/2 - line_size/2]
    corner_up_right= [width/2 + line_size/2, height/2 - line_size/2]
    corner_bottom_left = [width / 2 - line_size / 2, height / 2 + line_size / 2]
    corner_bottom_right = [width / 2 + line_size / 2, height / 2 + line_size / 2]

    return center, corner_up_left, corner_up_right, corner_bottom_left, corner_bottom_right



