import cv2 as cv
import numpy as np
import glob
import yaml
import image

line_color = (0, 255, 0)
line_thickness = 2
line_size = 25
fill_color = (0, 255, 0)

def calculate_pyramid(homography, image_base, image_test):
    mtx, dist = get_calibrations()
    h, w = image_base.shape[:2]
    #retval, rotations, translations, normals = cv.decomposeHomographyMat(homography, mtx)

    #scene_corners = np.zeros((4, 2), np.float32)
    print homography

    objp = np.zeros((5, 3), np.float32)
    objp[0] = [0, 0, 0]
    objp[1] = [-1, -1, 0]
    objp[2] = [-1, 1, 0]
    objp[3] = [1, 1, 0]
    objp[4] = [1, -1, 0]

    imagePoints = np.array(get_corners(image_base), np.float32)

    #retval, rvec, tvec = cv.solvePnP(objp, imagePoints, mtx, dist)


    # A TENTAR DESENHAR RETANGULO A VOLTA DE MAPA


    #pts = np.float32([[x, y]]).reshape(-1, 1, 2)
    obj_corners = np.array([[100, 100], [150, 100], [150, 150], [100, 150]], np.float32).reshape(-1, 1, 2)
    scene_corners = cv.perspectiveTransform(obj_corners, homography)
    #scene_corners = scene_corners[0]

    image_test = cv.line(image_test, tuple(scene_corners[0].ravel()), tuple(scene_corners[1].ravel()), line_color, line_thickness)
    image_test = cv.line(image_test, tuple(scene_corners[1].ravel()), tuple(scene_corners[2].ravel()), line_color, line_thickness)
    image_test = cv.line(image_test, tuple(scene_corners[2].ravel()), tuple(scene_corners[3].ravel()), line_color, line_thickness)
    image_test = cv.line(image_test, tuple(scene_corners[3].ravel()), tuple(scene_corners[0].ravel()), line_color, line_thickness)

    cv.imshow("tesssssst", image_test)
    cv.waitKey(0)


def draw_lines(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    height, width, channels = img.shape
    #corner = tuple([width/2, height/2])
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), line_color, line_thickness)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), line_color, line_thickness)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), line_color, line_thickness)
    img = cv.line(img, corner, tuple(imgpts[3].ravel()), line_color, line_thickness)

    img = cv.line(img, tuple(imgpts[0].ravel()), tuple(imgpts[1].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(imgpts[2].ravel()), tuple(imgpts[0].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(imgpts[1].ravel()), tuple(imgpts[3].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(imgpts[2].ravel()), tuple(imgpts[3].ravel()), line_color, line_thickness)
    return img

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


def get_corners(img):
    height, width, channels = img.shape
    center = [width/2, height/2]
    corner_up_left = [width/2 - line_size/2, height/2 - line_size/2]
    corner_up_right= [width/2 + line_size/2, height/2 - line_size/2]
    corner_bottom_left = [width / 2 - line_size / 2, height / 2 + line_size / 2]
    corner_bottom_right = [width / 2 + line_size / 2, height / 2 + line_size / 2]

    return np.array([center, corner_up_left, corner_up_right, corner_bottom_left, corner_bottom_right], np.float32)



