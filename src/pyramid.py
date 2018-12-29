import cv2 as cv
import numpy as np
import glob
import yaml
import utils
import image

line_color = (0, 0, 0)
line_thickness = 2
line_size = 20
fill_color = (0, 255, 0)


def calculate_pyramid(homography, image_test, pos_x, pos_y):

    '''
    Calculates the position of the pyramid and places it
    :param homography:
    :param image_test:
    :param pos_x:
    :param pos_y:
    :return:
    '''

    # get camera calibrations
    mtx, dist = get_calibrations()

    # decompose the homography into its various components
    retval, rotations, translations, normals = cv.decomposeHomographyMat(homography, mtx)

    # get the rotation vector from the rotation matrix
    rot = cv.Rodrigues(np.array(rotations))
    rotV = rot[0]

    # define the points in a 3D space
    objp = np.zeros((5, 3), np.float32)
    objp[0] = [0, 0, 1]
    objp[1] = [-1, -1, 0]
    objp[2] = [-1, 1, 1]
    objp[3] = [1, 1, 1]
    objp[4] = [1, -1, 0]

    # define the points of the image in a 2D space
    image_corners = get_corners(pos_x, pos_y)

    # find the object pose from a 3D to a 2D space
    retval, rotVector, translVector = cv.solvePnP(objp, image_corners, mtx, dist, rotV, np.array(translations))

    # project the points from 3D to 2D
    scene_corners, _ = cv.projectPoints(objp, rotV, np.array(translVector), mtx, dist)

    # draw the pyramid based on the calculated points
    draw_pyramid(image_test, scene_corners)


def draw_pyramid(img, corners):
    '''
    Draws the pyramid in the given image
    :param img:
    :param corners:
    :return:
    '''

    print(corners)
    # draw vertices
    cv.circle(img, tuple(corners[0].ravel()), 4, (255,0,255), line_thickness) # pink
    cv.circle(img, tuple(corners[1].ravel()), 4, (0,0,0), line_thickness) # black
    cv.circle(img, tuple(corners[2].ravel()), 4, (0,0,255), line_thickness) # red
    cv.circle(img, tuple(corners[3].ravel()), 4, (255,255,0), line_thickness) # cyan
    cv.circle(img, tuple(corners[4].ravel()), 4, (0,255,255), line_thickness) # yellow

    # fill pyramid base
    contours = np.array([corners[1].ravel(), corners[2].ravel(), corners[3].ravel(), corners[4].ravel()], 'int32')
    cv.fillPoly(img, pts=[contours], color=fill_color)

    # draw lines between corners
    img = cv.line(img, tuple(corners[4].ravel()), tuple(corners[1].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[1].ravel()), tuple(corners[2].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[2].ravel()), tuple(corners[3].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[3].ravel()), tuple(corners[4].ravel()), line_color, line_thickness)

    # draw lines between center and corners
    img = cv.line(img, tuple(corners[0].ravel()), tuple(corners[1].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[0].ravel()), tuple(corners[2].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[0].ravel()), tuple(corners[3].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[0].ravel()), tuple(corners[4].ravel()), line_color, line_thickness)


def get_corners(pos_x, pos_y):
    '''
    Gets the pyramid vertices based on the center point
    :param pos_x:
    :param pos_y:
    :return:
    '''

    vertex = [pos_x, pos_y - (2*line_size/3)]
    corner_up_right = [pos_x + line_size / 2, pos_y - line_size / 2]
    corner_up_left = [pos_x - line_size / 2, pos_y - line_size / 2]
    corner_bottom_left = [pos_x - line_size / 2, pos_y + line_size / 2]
    corner_bottom_right = [pos_x + line_size / 2, pos_y + line_size / 2]

    return np.array([vertex, corner_up_left, corner_bottom_left, corner_bottom_right, corner_up_right], np.float32)


def calibrate():
    '''
    Calibrates the camera with images from the chessboard folder, and saves the data into a yaml file
    '''
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    images = glob.glob('../resources/chessboard/*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (9, 6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (9, 6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    data = {'camera_matrix': np.asarray(mtx), 'dist_coeff': dist}

    print("Saving calibrations in file camera_calib.yaml")

    with open('../resources/calibrations/camera_calib.yaml', 'w') as f:
        yaml.dump(data, f)

    # calculate mean error -> the closer to 0, the better it is
    mean_error = 0
    for i in xrange(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error
    print("total error: {}" . format(mean_error / len(objpoints)))


def get_calibrations():
    '''
    Loads camera calibration data from file
    '''
    print("Loading camera calibrations from file")

    with open('../resources/calibrations/camera_calib.yaml') as f:
        calibrations = yaml.load(f)

    mtx = calibrations.get('camera_matrix')
    dist = calibrations.get('dist_coeff')

    return mtx, dist
