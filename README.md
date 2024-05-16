# Badminton Analysis

## Introduction

This project analyzes badminton players in a video to measure the Number of forehand and backhand shots, Force exerted on the shuttle, Shuttle Velocity and Time taken in each quadrant. This project will detect players and the shuttle using YOLO and also utilizes CNNs to extract court keypoints.

## Models Used

YOLO v5 for player detection

Fine Tuned YOLOv5 for shuttle detection

Court Key point extraction

Trained YOLOV5 model Data Used https://universe.roboflow.com/mathieu-cartron/shuttlecock-cqzy3/dataset/1/download

Trained badminton court key point model:

## Training

Shuttle detetcor with YOLOv5: training/shuttle_detector_training.ipynb

$ python3 train.py --data coco.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128


Badminton court keypoint with Pytorch: training/badminton_court_keypoints_training.ipynb

## Input Video

Drive Link: https://drive.google.com/file/d/1BRlbyLbf5xpHXbuPurqSLL6Hk3T1Tdmc/view?usp=sharing

### 1. Object Detection and Tracking:
**Approach**:
- **Detection**: YOLOv5 is used to detect badminton players, shuttlecock, and racket in each frame of the video.
- **Tracking**: Since YOLOv5 provides real-time object detection, there's no need for explicit tracking. The detected objects are considered as individual instances in each frame.

### 2. Force Exerted on the Shuttlecock:
**Approach**:
- **Velocity Calculation**: Using the positions of the shuttlecock in consecutive frames, we calculate its velocity, which is the rate of change of position over time.
- **Force Calculation**: Newton's second law of motion (Force = Mass * Acceleration) is applied to calculate the force exerted on the shuttlecock. The mass of the shuttlecock is assumed, and it's multiplied by its acceleration (change in velocity) to obtain the force.

### 3. Shot Classification:
**Approach**:
- **Racket Movement Analysis**: The movement of the player's racket relative to the shuttlecock is analyzed based on the detected positions.
- **Distance Calculation**: For each frame, the distance between the player's racket and the shuttlecock is calculated.
- **Shot Classification**: By comparing the distances between the racket and the shuttlecock in consecutive frames, the direction of movement (forehand or backhand) is determined.

### 4. Time Spent in Each Quadrant:
**Approach**:
- **Quadrant Definition**: The boundaries of the badminton court are divided into four quadrants: top-left, top-right, bottom-left, and bottom-right.
- **Quadrant Time Calculation**: As the shuttlecock moves, it's continuously checked if its position falls within the boundaries of each quadrant. When the shuttlecock crosses into a new quadrant, a timer starts to measure the time spent in that quadrant. This process repeats for each quadrant, and the cumulative time spent in each quadrant is recorded.

### 5. Shuttle Velocity
**Approach**:
The shuttle velocity is calculated based on the displacement of the shuttlecock over time.
Unit of this velocity would be pixel per second and we need the conversion factor to convert it into metre per second.
