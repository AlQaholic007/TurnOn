# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import time
import argparse
import imutils
import dlib
import cv2
import eye_local_fabian
import numpy as np
from scipy.spatial import distance as dist
import requests

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--camera", type=int, default=-1,
	help="which camera should be used")
args = vars(ap.parse_args())

# Global vars
FRAME_THRESHOLD = 10
RATIO_THRESHOLD_LB = 0.45
RATIO_THRESHOLD_UB = 0.55
COUNTER = 0
TRIGGERED = 0
MAX = 0
MIN = 100

# Draw boxes for eyes
def get_eye_box(eye):

    #print(eye)
    left = min(eye,key=lambda item:item[0])[0]
    right = max(eye, key=lambda item: item[0])[0]
    top = min(eye, key=lambda item: item[1])[1]
    bottom = max(eye, key=lambda item: item[1])[1]
    width = right - left
    height = bottom - top

    return (left, top, width, height)

# Determine the center of the eyes 
def eye_center(frame_grey, eyes):
    # x,y,width,height = face
    # faceROI = frame_grey[y:y+height, x:x+width]
    # cv2.imshow("Frame_face", faceROI)
    # cv2.namedWindow('Frame_face', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Frame_face', 600, 600)
    #
    # eyes = eye_cascade.detectMultiScale(faceROI)

    if len(eyes)>1:
        # print(len(eyes))
        (x1, y1, w1, h1) = eyes[0]

        # eyeROI1 =faceROI[y1:y1+h1, x1:x1+w1]
        # cv2.imshow("Frame_eye1", eyeROI1)
        # cv2.namedWindow('Frame_eye1', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Frame_eye1', 600, 600)
        #
        (x2, y2, w2, h2) = eyes[1]

        leftEyeROI = frame_grey[y1:y1+h1, x1:x1+w1]
        leftx = x1
        lefty = y1
        rightEyeROI = frame_grey[y2:y2+h2, x2:x2+w2]
        rightx = x2
        righty = x2

        # eyeROI2 = faceROI[y2:y2 + h2, x2:x2 + w2]
        # cv2.imshow("Frame_eye2", eyeROI2)
        # cv2.namedWindow('Frame_eye2', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Frame_eye2', 600, 600)
        # if(x1<x2):
        #     #cv2.imshow("Frame_eye1", eyeROI1)
        #     leftEyeROI = eyeROI2
        #     leftx = x2
        #     lefty = y2
        #     rightEyeROI = eyeROI1
        #     rightx = x1
        #     righty = y1
        # else:
        #     #cv2.imshow("Frame_eye2", eyeROI2)
        #     leftEyeROI = eyeROI1
        #     leftx = x1
        #     lefty = y1
        #     rightEyeROI = eyeROI2
        #     rightx = x2
        #     righty = y2
        #print(eyeROI1.shape)

        #localframe = cv2.imread("Eye.jpg")
        # frame = imutils.resize(frame, width=450)
        #eyeImg = cv2.cvtColor(localframe, cv2.COLOR_BGR2GRAY)
        eyeImg = leftEyeROI.astype(np.float32)

        coord = eye_local_fabian.findEyeCenter(eyeImg,0)

        cv2.circle(leftEyeROI, coord, 1, (255,255,255), -1 )
        cv2.imshow("Frame_STUFF", leftEyeROI)

        return (coord[0]+x1, coord[1]+y1)

    return (0,0)

# Calculate GCR for detecting rapid change
def gaze_corner_ratio(eye, center):

    bottom_right_dist = dist.euclidean(eye[0], center) + dist.euclidean(eye[5], center)
    top_left_dist = dist.euclidean(eye[2], center) + dist.euclidean(eye[3], center)

    return bottom_right_dist/top_left_dist

# Get the ratio of eye at the left bottom of the screen ( bottom right of real eye )
def bottom_left_region(eye, center):

    x_ratio  = (center[0] - eye[0][0])/(eye[3][0] - eye[0][0])
    y_ratio  = (eye[5][1] - center[1])/(eye[5][1] - eye[1][1])

    return (x_ratio, y_ratio)

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
eye_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
# print(args["camera"])
vs = VideoStream(args["camera"]).start()
time.sleep(2.0)

# Get the index of facial landmarks
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    frame = vs.read()
    # frame = cv2.imread("face.jpeg")
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Get left and right eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # generate boxes for left/right eyes
        (lx, ly, lw, lh) = get_eye_box(leftEye)
        (rx, ry, rw, rh) = get_eye_box(rightEye)
        eyeboxes = [(lx, ly, lw, lh), (rx, ry, rw, rh)]

        # Draw rectangle for eyes and face for testing purpose
        cv2.rectangle(frame, (lx, ly), (lx + lw, ly + lh), (0, 255, 255), 2)
        cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (255, 255, 0), 2)
        cv2.rectangle(frame, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (255, 0, 0), 2)
        #detected = eye_cascade.detectMultiScale(gray, 1.3, 5)

        # Determine and draw the center of the left eye
        (lcenterx, lcentery) = eye_center(gray, eyeboxes)
        cv2.circle(frame, (lcenterx, lcentery), 1, (255, 255, 255), -1)

        # gcr is one of the implementation that detects more on rate of change rather than absolute value
        #gcr_result = gaze_corner_ratio(leftEye, (lcenterx, lcentery))

        # Calculate absolute ratio for left eye center
        (xratio, yratio) = bottom_left_region(leftEye, (lcenterx, lcentery))

        # Count the center of X in threshold
        if RATIO_THRESHOLD_LB<xratio<RATIO_THRESHOLD_UB:
            COUNTER += 1
        else:
            if COUNTER >= FRAME_THRESHOLD:
                TRIGGERED += 1

                # reset the eye frame counter
                COUNTER = 0

        # Calculate the MIN and MAX eye height can possibly be for testing
        if (leftEye[5][1] - leftEye[1][1])>MAX:
            MAX = leftEye[5][1] - leftEye[1][1]

        if (leftEye[5][1] - leftEye[1][1])<MIN:
            MIN = leftEye[5][1] - leftEye[1][1]

        # Output texts
        cv2.putText(frame, "X%: {}".format(xratio), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Y%: {}".format(yratio), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, "TRIG: {}".format(TRIGGERED), (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, "MAX: {}".format(MAX), (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, "MIN: {}".format(MIN), (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)


    # show the frame for testing
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # Uncomment this line for localhost testing
    # if TRIGGERED >= 2:
    #     print("POST SENT")
    #     resp = requests.post("http://172.16.46.128:3000/flip", json={"flip":True} )
    #     pprint(resp)
    #     # if (resp.confirm == True):
    #     resp = requests.get("http://172.16.46.128:3000/flip")
    #     while resp.json() != True:
    #         pprint(resp.text)
    #         pprint(resp.content)
    #         pprint(resp.json())
    #         resp = requests.get("http://172.16.46.128:3000/flip")
    #         input("heyya")
    #         continue
    #     TRIGGERED = 0

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
