import cv2 as cv


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

