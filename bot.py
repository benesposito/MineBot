from builtins import filter

from directkeys import *
from grabscreen import grab_screen
import time
import cv2
import numpy as np

def nothing(x):
    pass

# cv2.namedWindow('threshold_tester')
# cv2.namedWindow('contours_tester')
cv2.createTrackbar('h', 'threshold_tester', 0, 180, nothing)
cv2.createTrackbar('s', 'threshold_tester', 0, 255, nothing)
cv2.createTrackbar('v', 'threshold_tester', 0, 255, nothing)
cv2.createTrackbar('H', 'threshold_tester', 0, 180, nothing)
cv2.createTrackbar('S', 'threshold_tester', 0, 255, nothing)
cv2.createTrackbar('V', 'threshold_tester', 0, 255, nothing)
cv2.createTrackbar('dilations', 'threshold_tester', 0, 10, nothing)
cv2.createTrackbar('erosions', 'threshold_tester', 0, 10, nothing)
cv2.createTrackbar('max area', 'contours_tester', 0, 10000, nothing)
cv2.createTrackbar('min area', 'contours_tester', 0, 10000, nothing)

#PressKey(W)
# H: 0 - 180
# S: 0 - 255
# V: 0 - 255

lower_thresh_lava = np.array([9, 194, 84])
upper_thresh_lava = np.array([14, 245, 219])

lower_thresh_diamond = np.array([84, 42, 9])
upper_thresh_diamond = np.array([106, 170, 32])

lower_thresh_iron = np.array([0, 54, 5]) # fix gravel
upper_thresh_iron = np.array([98, 145, 24])

cv2.setTrackbarPos('h', 'threshold_tester', lower_thresh_diamond[0])
cv2.setTrackbarPos('s', 'threshold_tester', lower_thresh_diamond[1])
cv2.setTrackbarPos('v', 'threshold_tester', lower_thresh_diamond[2])
cv2.setTrackbarPos('H', 'threshold_tester', upper_thresh_diamond[0])
cv2.setTrackbarPos('S', 'threshold_tester', upper_thresh_diamond[1])
cv2.setTrackbarPos('V', 'threshold_tester', upper_thresh_diamond[2])

kernel = np.ones((5, 5), np.uint8)

paused = True
screen = grab_screen(region=(0, 35, 854, 510))
cv2.imshow('screen', screen)

lava_spasm = True
debounce = time.time()
last_time = time.time()
last_lava_seen = 0
while True:
    if not paused:
        screen = grab_screen(region=(0, 35, 854, 510))
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        h = cv2.getTrackbarPos('h', 'threshold_tester')
        s = cv2.getTrackbarPos('s', 'threshold_tester')
        v = cv2.getTrackbarPos('v', 'threshold_tester')
        H = cv2.getTrackbarPos('H', 'threshold_tester')
        S = cv2.getTrackbarPos('S', 'threshold_tester')
        V = cv2.getTrackbarPos('V', 'threshold_tester')
        dilations = cv2.getTrackbarPos('dilations', 'threshold_tester')
        erosions = cv2.getTrackbarPos('erosions', 'threshold_tester')
        max_area = cv2.getTrackbarPos('max area', 'contours_tester')
        min_area = cv2.getTrackbarPos('min area', 'contours_tester')

        threshold_test = cv2.inRange(hsv, np.array([h, s, v]), np.array([H, S, V]))
        dilated_test = cv2.dilate(threshold_test, kernel, iterations=dilations)
        eroded_test = cv2.erode(dilated_test, kernel, iterations=erosions)

        lava_threshold = cv2.inRange(hsv, lower_thresh_lava, upper_thresh_lava)
        lava_dilated = cv2.dilate(lava_threshold, kernel, iterations=3)
        lava_eroded = cv2.erode(lava_dilated, kernel, iterations=1)
        lava_contours_image, lava_contours, lava_hierarchy = cv2.findContours(lava_eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered_lava_contours = []

        for c in lava_contours:
            if cv2.contourArea(c) > 500:
                filtered_lava_contours.append(c)

        diamond_threshold = cv2.inRange(hsv, lower_thresh_diamond, upper_thresh_diamond)
        diamond_dilated = cv2.dilate(diamond_threshold, kernel, iterations=1)
        diamond_contours_image, diamond_contours, diamond_hierarchy = cv2.findContours(diamond_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered_diamond_contours = []
        [filtered_diamond_contours.append(c) for c in diamond_contours]# if cv2.contourArea(c) < max_area and cv2.contourArea(c) > min_area]

        iron_threshold = cv2.inRange(hsv, lower_thresh_iron, upper_thresh_iron)
        iron_dilated = cv2.dilate(iron_threshold, kernel, iterations=3)
        iron_contours_image, iron_contours, iron_hierarchy = cv2.findContours(iron_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered_iron_contours = []

        [filtered_iron_contours.append(c) for c in iron_contours if cv2.contourArea(c) < max_area and cv2.contourArea(c) > min_area]

        cv2.drawContours(screen, filtered_lava_contours, -1, (0, 0, 255), 2)
        cv2.drawContours(screen, filtered_diamond_contours, -1, (255, 250, 0), 2)
        # cv2.drawContours(screen, filtered_iron_contours, -1, (158, 174, 223), 2)

        cv2.imshow('screen', screen)

        if len(filtered_lava_contours) > 0 and time.time() - last_lava_seen < 2:
            mouseUp('left')
            ReleaseKey('SHIFT')
            ReleaseKey('W')
            PressKey('S')
            mouseDown('right')
            last_lava_seen = time.time()
        elif time.time() - last_lava_seen < 3:
            rotate('right')
        else:
            mouseUp('right')
            ReleaseKey('S')
            keyPWM('W')
            PressKey('SHIFT')
            mouseDown()

        print('{} fps'.format(1.0 / (time.time()-last_time)))
        last_time = time.time()

    if getKey('Z') and getKey('X') and time.time() - debounce > 0.5:
        paused = not paused
        debounce = time.time()
        if paused:
            ReleaseKey('W')
            ReleaseKey('S')
            ReleaseKey('SHIFT')
            mouseUp()
            mouseUp('right')

    if cv2.waitKey(5) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
