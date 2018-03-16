# Parking Lot and Spot Finder
The first satellite photograph of the Earth is a grainy, black and white photo taken on August 14, 1959 by the US Explorer 6. Since then, both the quality and quantity of satellite imagery has dramatically increased. Today, the problem is too much data. Map features such as roads, buildings, and other points of interest are mainly extracted manually, and we just don’t have enough humans to carry out this mundane task.

The goal of this project is to develop a tool that automates this process. Although a wide range of features can be extracted using Object Based Imagery Analysis, the focus of this project will be parking lots. Students are challenged with developing a Python tool/script that uses Machine Learning algorithms to identify and extract parking lots and their usage (taken spots vs. total spots) from high resolution satellite imagery.

This project will be divided into two main phases, each focused on labeling data and training an algorithm to identify parking lots and the parking spaces within each parking lot. The first stage of each phase will focused on labeling the training data. We will manually analyze satellite imagery and generate a GeoJSON or Shapefile denoting the parking lots it contains and the usage of those parking lots. During the second stage we will implement the learning algorithm for identifying the parking lot/spaces. The two phases should result in a tool that can take in satellite imagery and output a GeoJSON or Shapefile denoting each parking lot and its usage. 

### Process
We will start out trying to detect parking lots from satellite images. The first part will be processing and labeling the images. Images will be retrieved from SpaceNet and we will process and label it. The second part will be developing algorithm to recognize which images contain parking lots. 
Stretch goals will be to do the exact same thing but detect whether or not the park lots have empty space in them.
### Input and Output
Input: We expect input to be satellite images with specific dimension. The images may or may not contain parking lots.
Output: Initial output would be boolean values indicating whether or not the inputted images contain parking lots.

### Resources:
Slides on Caffe:
http://tutorial.caffe.berkeleyvision.org/caffe-cvpr15-detection.pdf
https://docs.google.com/presentation/d/1HxGdeq8MPktHaPb-rlmYYQ723iWzq9ur6Gjo71YiG0Y/edit#slide=id.gc2fcdcce7_216_438
Video on Caffe:
https://www.youtube.com/watch?v=rvMVqPsXL10
### Caffe Fast-RCNN: 
https://github.com/rbgirshick/caffe-fast-rcnn
