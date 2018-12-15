import cv2 as cv


def get_features(image):
    """
    FAST feature extract & display
    """
    fast = cv.FastFeatureDetector_create()
    fast_kp = fast.detect(image, None)
    fast_display = cv.drawKeypoints(image, fast_kp, None)
    cv.imshow('fast', fast_display)

