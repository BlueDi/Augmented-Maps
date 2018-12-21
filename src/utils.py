import cv2 as cv
import numpy as np
import math


def kp_to_list(kp):
    """
    Transform a KeyPoint to a list
    The KeyPoint can not be saved as a pickle
    Need to transform it to a list first
    """
    kp_list = []
    for point in kp:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id) 
        kp_list.append(temp)
    return kp_list


def list_to_kp(kp_list):
    """
    Transform a list to a KeyPoint
    The KeyPoint was saved as a list to be stored in a pickle
    Need to transform it back to a KeyPoint to use it
    """
    kp = []
    for point in kp_list:
        temp = cv.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5]) 
        kp.append(temp)
    return kp

def map_coordinates(matrix, x, y):
    origin = np.array([[x], [y], [1]])
    points = np.matmul(matrix, origin)
    pX = int(round(points[0]/points[2]))
    pY = int(round(points[1]/points[2]))
    return pX, pY

def calculate_distance(x1, y1, x2, y2):
    dist = math.hypot(x1 - x2, y1 - y2)
    return dist