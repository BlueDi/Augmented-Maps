import cv2 as cv
import numpy as np


def get_features(image):
    """
    KAZE feature extract & display
    """
    kaze = cv.KAZE_create()
    kaze_kp, kaze_desc = kaze.detectAndCompute(image, None)
    kaze_display = cv.drawKeypoints(image, kaze_kp, None)
    cv.imshow('kaze', kaze_display)


def filter_matches_by_distance(matches):
    """
    Remove the most distant matching points
    """
    filteredMatches = []
    matches = sorted(matches, key = lambda x:x.distance)
    ptsPairs = min(400, len(matches) * 0.3)
    filteredMatches = matches[:int(ptsPairs)]
    return filteredMatches


def filter_matches_RANSAC(matches, keypointsA, keypointsB):
    filteredMatches = []
    if len(matches) >= 4:
        src_pts = np.float32([ keypointsA[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ keypointsB[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        homography, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 1.0)
        matchesMask = mask.ravel().tolist()

        for i in range(len(matchesMask)):
            if matchesMask[i] == 1:
                filteredMatches.append(matches[i])

    return homography, filteredMatches


def match_results(image1, image2):
    """
    Match features from 2 images
    First extract KAZE features of both images
    Then match the returned features
    """
    detector = cv.KAZE_create()
    matcher = cv.FlannBasedMatcher()
    kaze_kp1, kaze_desc1 = detector.detectAndCompute(image1, None)
    kaze_kp2, kaze_desc2 = detector.detectAndCompute(image2, None)
    matches = matcher.match(kaze_desc1, kaze_desc2)
    distance_matches = filter_matches_by_distance(matches)
    homography, filtered_matches = filter_matches_RANSAC(distance_matches, kaze_kp1, kaze_kp2)
    return image1, kaze_kp1, image2, kaze_kp2, filtered_matches, homography

