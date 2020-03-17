# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time

# HSV color range
orange_upper = (120, 255, 255)
orange_lower = (105, 175, 190)

# Grab Camera Stream
vs = None


def update_color(upper, lower):
    global orange_lower, orange_upper

    index = 0
    for field in upper:
        upper[index] = orange_upper[index] if field is None else field
        index += 1

    index = 0
    for field in lower:
        lower[index] = orange_lower[index] if field is None else field
        index += 1

    orange_lower = tuple(lower)
    orange_upper = tuple(upper)


class Tracking:
    mask, frame = (None,)*2

    def __init__(self, existingVS=None):
        global vs
        # Initiate stream if not already done
        vs = VideoStream(src=0).start() if existingVS is None else existingVS
        self.frame = vs.read()
        # Allow Camera to warm up
        time.sleep(1.0)

    def detect(self):
        global orange_upper, orange_lower, vs

        # Grab Current Frame
        self.frame = vs.read()

        # Resize the frame, blur it, convert to HSV colorspace
        self.frame = imutils.resize(self.frame, width=1000)
        blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)

        # Construct a mask for the orange ball
        self.mask = cv2.inRange(hsv, orange_lower, orange_upper)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mask = cv2.dilate(self.mask, None, iterations=2)

        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(self.frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(self.frame, center, 5, (0, 0, 255), -1)

    def get_frame(self):
        return self.frame

    def get_HSV(self):
        return (orange_upper, orange_lower).__str__()
