# TurnOn is a smart page turner that automates eye gaze tracking for assistive reading using OpenCV

## Following libraries were used for eye tracking

- OpenCV
- dlib
- numpy
- imutils
- scipy
- shape_predictor_68_face_landmarks.dat 

#### Use the following command to run the python module
```
python landmark_with_center.py --shape-predictor shape_predictor_68_face_landmarks.dat --camera 0
```
*You can change the camera parameter to 1 if you wish to use an external webcam


#### Use the following to configure threshold for detection
```
FRAME_THRESHOLD = 10
RATIO_THRESHOLD_LB = 0.45
RATIO_THRESHOLD_UB = 0.55
```

## Web host
Web application for simple proof of concept of page turning.

To run the web application, first run  
```
ifconfig   (LINUX)
ipconfig   (WINDOWS)
```
to get your ip address and swap it within `index.html` file

Then run
```
npm install
node app.js
```
