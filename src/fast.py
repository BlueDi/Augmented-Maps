import cv2 as cv


def fast_get_features(image):
    """
    First part of exercises
    FAST & KAZE feature extract & display
    """
    fast = cv.FastFeatureDetector_create()
    fast_kp = fast.detect(image, None)
    fast_display = cv.drawKeypoints(image, fast_kp, None)
    cv.imshow('fast', fast_display)

