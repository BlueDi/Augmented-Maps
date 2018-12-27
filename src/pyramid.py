import cv2 as cv
import numpy as np
import glob
import yaml
import utils
import image

line_color = (0, 250, 0)
line_thickness = 2
line_size = 22
fill_color = (255, 255, 0)


def calculate_pyramid(homography, image_base, image_test, pos_x, pos_y):

    # buscar as calibracoes da camara
    mtx, dist = get_calibrations()

    # decompor a homografia nas varias componentes
    retval, rotations, translations, normals = cv.decomposeHomographyMat(homography, mtx)

    #obter o vetor de rotacoes a partir da matriz de rotacoes
    rot = cv.Rodrigues(np.array(rotations))

    # definir os pontos num espaco 3d - ERRO AQUI
    objp = np.zeros((5, 3), np.float32)
    objp[0] = [0, 0, 1]
    objp[1] = [-1, -1, 0]
    objp[4] = [1, -1, 0]
    objp[3] = [1, 1, 0]
    objp[2] = [-1, 1, 0]

    # definir os pontos da imagem num espaco 2d
    image_corners = get_corners(pos_x, pos_y)
    #image_corners = np.array([[580, 260], [560, 240], [560, 280], [600, 280], [600, 240]], np.float32)
    rotV = rot[0]

    # encontrar a pose do objeto de um espaco 3d para 2d
    retval, rotVector, translVector = cv.solvePnP(objp, image_corners, mtx, dist, rotV, np.array(translations))

    print('rotVector: ' + str(rotVector))
    print('translVector: ' + str(translVector))
    print('camera matrix: ' + str(mtx))
    print('dist coeffs: ' + str(dist))

    # projetar os pontos de 3d para 2d
    scene_corners, _ = cv.projectPoints(objp, rotV, np.array(translVector), mtx, dist)

    # desenhar a piramide com base nos pontos calculados
    draw_pyramid(image_test, scene_corners)

    #cv.imshow("tesssssst", image_test)
    #cv.waitKey(0)


def draw_pyramid(img, corners):
    cv.circle(img, tuple(corners[0].ravel()), 4, line_color, line_thickness)
    cv.circle(img, tuple(corners[1].ravel()), 4, (0,0,0), line_thickness)
    cv.circle(img, tuple(corners[2].ravel()), 4, (0,0,255), line_thickness)
    cv.circle(img, tuple(corners[3].ravel()), 4, (255,255,0), line_thickness)
    cv.circle(img, tuple(corners[4].ravel()), 4, (0,255,255), line_thickness)

    # desenhar linhas
    img = cv.line(img, tuple(corners[0].ravel()), tuple(corners[1].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[1].ravel()), tuple(corners[2].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[2].ravel()), tuple(corners[3].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[3].ravel()), tuple(corners[0].ravel()), line_color, line_thickness)

    img = cv.line(img, tuple(corners[4].ravel()), tuple(corners[0].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[4].ravel()), tuple(corners[1].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[4].ravel()), tuple(corners[2].ravel()), line_color, line_thickness)
    img = cv.line(img, tuple(corners[4].ravel()), tuple(corners[3].ravel()), line_color, line_thickness)

    #corners_new = np.array([corners[0].ravel(), corners[1].ravel(), corners[2].ravel(), corners[3].ravel()])
    #cv.fillPoly(img, pts=corners_new, color=fill_color)

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


def get_corners(pos_x, pos_y):
    center = [pos_x, pos_y]
    corner_up_right = [pos_x + line_size / 2, pos_y - line_size / 2]
    corner_up_left = [pos_x - line_size / 2, pos_y - line_size / 2]
    corner_bottom_left = [pos_x - line_size / 2, pos_y + line_size / 2]
    corner_bottom_right = [pos_x + line_size / 2, pos_y + line_size / 2]

    return np.array([center, corner_up_left, corner_bottom_left, corner_bottom_right, corner_up_right], np.float32)



