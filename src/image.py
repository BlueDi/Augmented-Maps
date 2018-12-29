import cv2 as cv
import numpy as np
import utils

def open_image_for_process(filename):
    """Opens the image as gray scale"""
    try:
        image = cv.imread(filename)
        image = image_resize(image)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    except:
        print(" --(!) Error reading image ", filename)
        return None
    return image

def open_image_for_display(filename):
    """Opens the image for display"""
    try:
        image = cv.imread(filename)
        image = image_resize(image)
    except:
        print(" --(!) Error reading image ", filename)
        return None
    return image


def image_resize(image, width = None, height = None, inter = cv.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    if(w >= h and w > 1000):
        width = 1000
    elif(w < h and h > 1000):
        height = 650

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized