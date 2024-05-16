# Badminton Analysis

## Introduction

This project analyzes badminton players in a video to measure the Number of forehand and backhand shots, Force exerted on the shuttle, Shuttle Velocity and Time taken in each quadrant. This project will detect players and the shuttle using YOLO and also utilizes CNNs to extract court keypoints.

## Models Used

YOLO v8 for player detection

Fine Tuned YOLO for shuttle detection

Court Key point extraction

Trained YOLOV5 model: 
Trained badminton court key point model:

## Training

Shuttle detetcor with YOLO: training/shuttle_detector_training.ipynb

Badminton court keypoint with Pytorch: training/badminton_court_keypoints_training.ipynb

