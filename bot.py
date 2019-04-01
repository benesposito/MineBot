from builtins import filter

from directkeys import *
from grabscreen import grab_screen
import time
import cv2
import numpy as np

lower_thresh_lava = np.array([0, 169, 115])
upper_thresh_lava = np.array([49, 255, 255])

lower_thresh_diamond = np.array([84, 42, 9])
upper_thresh_diamond = np.array([106, 170, 32])

lower_thresh_iron = np.array([0, 54, 5]) # fix gravel
upper_thresh_iron = np.array([98, 145, 24])

kernel = np.ones((5, 5), np.uint8)

paused = True
cv2.imshow('screen', cv2.resize(grab_screen(), (640, 360)))

lava_spasm = True
debounce = time.time()
last_time = time.time()
last_lava_seen = 0
while True:
    screen = cv2.resize(grab_screen(), (640, 360))
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

    lava_threshold = cv2.inRange(hsv, lower_thresh_lava, upper_thresh_lava)
    lava_dilated = cv2.dilate(lava_threshold, kernel, iterations=0)
    lava_eroded = cv2.erode(lava_dilated, kernel, iterations=0)
    lava_contours, lava_hierarchy = cv2.findContours(lava_eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_lava_contours = []

    for c in lava_contours:
        if cv2.contourArea(c) > 500:
            filtered_lava_contours.append(c)

    '''
    diamond_threshold = cv2.inRange(hsv, lower_thresh_diamond, upper_thresh_diamond)
    diamond_dilated = cv2.dilate(diamond_threshold, kernel, iterations=1)
    diamond_contours, diamond_hierarchy = cv2.findContours(diamond_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_diamond_contours = []
    [filtered_diamond_contours.append(c) for c in diamond_contours]# if cv2.contourArea(c) < max_area and cv2.contourArea(c) > min_area]

    iron_threshold = cv2.inRange(hsv, lower_thresh_iron, upper_thresh_iron)
    iron_dilated = cv2.dilate(iron_threshold, kernel, iterations=3)
    iron_contours, iron_hierarchy = cv2.findContours(iron_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_iron_contours = []

    [filtered_iron_contours.append(c) for c in iron_contours if cv2.contourArea(c) < max_area and cv2.contourArea(c) > min_area]
    '''

    cv2.drawContours(screen, filtered_lava_contours, -1, (0, 0, 255), 2)
    # cv2.drawContours(screen, filtered_diamond_contours, -1, (255, 250, 0), 2)
    # cv2.drawContours(screen, filtered_iron_contours, -1, (158, 174, 223), 2)

    cv2.imshow('screen', screen)
    print('Paused: {}'.format(paused))
    print('Lava contours #: {}'.format(len(filtered_lava_contours)))
    print('Last lava: {}'.format(time.time() - last_lava_seen))

    if not paused:
        if len(filtered_lava_contours) > 0:
            last_lava_seen = time.time()

            if time.time() - last_lava_seen < 2:
                mouseUp('left')
                ReleaseKey('SHIFT')
                ReleaseKey('W')
                PressKey('S')
                mouseDown('right')
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
