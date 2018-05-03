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

### Tutorial
I. Software Installation

A. Training model
Install Cuda & cuDNN
Cuda Installation Guide: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/
CuDNN Installation Guide: https://docs.nvidia.com/deeplearning/sdk/cudnn-install/
Install Tensorflow
Tensorflow Installation Instructions: https://www.tensorflow.org/install/ 
Install Additional Python Dependencies:
Install pillow, lxml, jupyter, matplotlib
Retrieve & Make Tensorflow Models:
Git clone the following repository: https://github.com/tensorflow/models
If using Ubuntu navigate to models/research and execute command: protoc object_detection/protos/*.proto --python_out=. And export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
Retrieve Our Code:
Git clone the following repository: https://github.com/khoale95/SatImageParkingLotFinder

B. Labelling
Follow the steps we detailed in the implementation section (Section V) for labelling data. The future work section details labelling rotated bounding boxes for use in the DRBox model.

LabelImg: Download and use LabelImg at https://github.com/tzutalin/labelImg  
roLabelImg: Download and use roLabelImg at https://github.com/cgvict/roLabelImg . For roLabelImg, you want to always use the rotating bounding box as the normal bounding boxes does not store an angle in the output XML file.

II. Training on New Data

In order to train the object detection once information has been labeled using LabelImg a few steps must be taken.

A. Data Manipulation
Put LabelImg xml files into the bounding boxes folder.
Put your JPEG’s into the images folder
Run xml_to_csv.py
Run splittraintest.py with the arguments of the csv file name and ratio of training to testing. For example python splittraintest.py data/parkinglot_labels.csv 0.8 will create a test and train split of the overall csv file with 80% of the training images being part of the training set.
Create tfrecords for use by the neural network
Run: python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record
Run: python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
The information is now formatted in the correct way to be passed to the neural network.

B. Model Setup
Locate a model you want to use on: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
Add the .config file to the training directory. We used faster_rcnn_resnet101_kitti.config. The model selected can differ based on training needs.
Once you have downloaded the config file you will need to adjust the necessary paths and parameters to your data. Reference faster_rcnn_resnet101_kitti.config in the repo as an example.
If interested you can also acquire model checkpoints. To use these download the tar file and extract them in Tensorflow’s model/research/object_detection directory.
In the training directory create an object-detection.pbtxt file. It should look something like:
 item {
     id: 1
      name: 'parking lot'
}

C. Running Model
All setup has now been completed and training can begin
To train navigate to models/research/object_detection and run python train.py --logtostderr  --train_dir=training/ --pipeline_config_path=training/faster_rcnn_resnet101_kitti.config
To monitor the progress you can run tensorboard --logdir=’training’ from models/object_detection
NOTE: The directory training is the one provided in our repository, your path to get there may have to have precursors. For example: /home/user/Documents/SatImageParkingLotFinder/training


### Resources:
Slides on Caffe:
http://tutorial.caffe.berkeleyvision.org/caffe-cvpr15-detection.pdf
https://docs.google.com/presentation/d/1HxGdeq8MPktHaPb-rlmYYQ723iWzq9ur6Gjo71YiG0Y/edit#slide=id.gc2fcdcce7_216_438
https://cs.nyu.edu/~yann/talks/lecun-ranzato-icml2013.pdf

Video on Caffe:
https://www.youtube.com/watch?v=rvMVqPsXL10

### Caffe Fast-RCNN: 
https://github.com/rbgirshick/caffe-fast-rcnn

### Caffe Faster-RCNN: 
https://github.com/rbgirshick/py-faster-rcnn

### Resources for deep learning:
https://www.youtube.com/channel/UCeqlHZDmUEQQHYqnei8doYg/featured

### Fast R-CNN own data guide:
https://github.com/deboc/py-faster-rcnn/tree/master/help
