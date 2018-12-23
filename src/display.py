import cv2 as cv
import numpy as np
import image as img
import utils
import os
import re

CIRCLE_SIZE = 7
CURRENT = 0

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
    pass

def place_center(image, x, y):
    cv.circle(image, (x,y), 7, (19, 255, 255), -1)
    cv.circle(image, (x,y), 7, (0,0,0), 1)
    pass


def place_compass(inverse, image_test, xCenter, yCenter, xInterest, yInterest):
    '''
    Calcular coordenadas do centro da bussola
    '''
    
    interest_quadrantX = xInterest - xCenter
    interest_quadrantY = yInterest - yCenter

    X_OFFSET = 50
    Y_OFFSET = 50

    compassCenter = [xCenter, yCenter]

    if interest_quadrantX > 0 and interest_quadrantY < 0:
        compassCenter[0] -= X_OFFSET
        compassCenter[1] += Y_OFFSET
        pass
    elif interest_quadrantX < 0 and interest_quadrantY < 0:
        compassCenter[0] += X_OFFSET
        compassCenter[1] += Y_OFFSET
        pass
    elif interest_quadrantX < 0 and interest_quadrantY > 0:
        compassCenter[0] += X_OFFSET
        compassCenter[1] -= Y_OFFSET
        pass
    elif interest_quadrantX > 0 and interest_quadrantY > 0:
        compassCenter[0] -= X_OFFSET
        compassCenter[1] -= Y_OFFSET
        pass
    elif interest_quadrantX == 0 and interest_quadrantY > 0:
        compassCenter[1] -= Y_OFFSET
        pass
    elif interest_quadrantX == 0 and interest_quadrantY < 0:
        compassCenter[1] += Y_OFFSET
        pass
    elif interest_quadrantX > 0 and interest_quadrantY == 0:
        compassCenter[0] -= X_OFFSET
        pass
    elif interest_quadrantX < 0 and interest_quadrantY == 0:
        compassCenter[0] += X_OFFSET
        pass
    else:
        compassCenter[0] += X_OFFSET
        compassCenter[1] += Y_OFFSET
        pass
    
    '''
    Retirar cordenada do topo, meio e baixo, meio
    '''
    COMPASS_H = 50
    COMPASS_W = 10

    compassTop = [compassCenter[0], compassCenter[1]+COMPASS_H]
    compassDown = [compassCenter[0], compassCenter[1]-COMPASS_H]
    compassLeft = [compassCenter[0]-COMPASS_W, compassCenter[1]]
    compassRight = [compassCenter[0]+COMPASS_W, compassCenter[1]]
    '''
    Conveter para coordenadas para original
    '''

    originalTopX, originalTopY = utils.map_coordinates(inverse, compassTop[0], compassTop[1])
    originalDownX, originalDownY = utils.map_coordinates(inverse, compassDown[0], compassDown[1])

    '''
    calcular angulo entre os vetores
    '''
    angle = utils.angle(compassTop[0], compassTop[1], compassDown[0],compassDown[1], originalTopX, originalTopY, originalDownX, originalDownY)
    angle = -angle

    '''
    Calcular novos pontos do compass
    '''
    xTop, yTop = utils.rotate((compassCenter[0], compassCenter[1]),(compassTop[0], compassTop[1]), angle)
    xDown, yDown = utils.rotate((compassCenter[0], compassCenter[1]),(compassDown[0], compassDown[1]), angle)
    xLeft, yLeft = utils.rotate((compassCenter[0], compassCenter[1]),(compassLeft[0], compassLeft[1]), angle)
    xRight, yRight = utils.rotate((compassCenter[0], compassCenter[1]),(compassRight[0], compassRight[1]), angle)

    xTop = int(round(xTop))
    yTop = int(round(yTop))
    xDown = int(round(xDown))
    yDown = int(round(yDown))
    xLeft = int(round(xLeft))
    yLeft = int(round(yLeft))
    xRight = int(round(xRight))
    yRight = int(round(yRight))

    '''
    Desenhar primeiro triangulo
    '''
    triangle_cnt_1 = np.array( [(xTop, yTop), (xLeft, yLeft), (xRight, yRight)] )
    cv.drawContours(image_test, [triangle_cnt_1], 0, (255,0,0), -1)

    '''
    Desenhar segundo triangulo
    '''
    triangle_cnt_2 = np.array( [(xDown, yDown), (xLeft, yLeft), (xRight, yRight)] )
    cv.drawContours(image_test, [triangle_cnt_2], 0, (0,0,255), -1)
    pass

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


def transition(event, x, y, flags, param):
    
    if event ==  cv.EVENT_LBUTTONUP:
        windowName, images = param
        global CURRENT
        CURRENT += 1
        if CURRENT >= len(images):
            CURRENT = 0
        image = cv.imread(images[CURRENT],cv.IMREAD_UNCHANGED)
        cv.namedWindow(windowName)
        cv.imshow(windowName, image)

def create_slideshow(name, distance_km, IMAGE_FOLDER):
    
    pattern = name + '*'
    prog = re.compile(pattern)
    images = []
    
    for _, _, files in os.walk(IMAGE_FOLDER):  
        for filename in files:
            if prog.match(filename) is not None:
                images.append(os.path.join(IMAGE_FOLDER, filename))

    if len(images) <= 0:
        return

    windowName = name + " - " + str(int(round(distance_km))) + " m"
    image = cv.imread(images[0],cv.IMREAD_UNCHANGED)
    cv.namedWindow(windowName)
    cv.imshow(windowName, image)
    cv.setMouseCallback(windowName, transition, (windowName, images))



