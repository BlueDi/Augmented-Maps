import cv2 as cv
import numpy as np
import numpy.linalg as la
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
    pts = np.float32([[x,y]]).reshape(-1,1,2)
    dst = cv.perspectiveTransform(pts, matrix)
    pX = int(round(dst[0][0][0]))
    pY = int(round(dst[0][0][1]))
    return pX, pY

def calculate_distance(x1, y1, x2, y2):
    dist = math.hypot(x1 - x2, y1 - y2)
    return dist

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(x1,y1,x2,y2,x3,y3,x4,y4):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1 = (x2-x1, y2-y1)
    v2 = (x4-x3, y4-y3)
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def angle(px1,py1,px2,py2,px3,py3,px4,py4):

    x1 = px2 - px1
    y1 = py2 - py1
    x2 = px4 - px3
    y2 = py4 - py3

    dot = x1*x2 + y1*y2   
    det = x1*y2 - y1*x2  
    return math.atan2(det, dot) 

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy