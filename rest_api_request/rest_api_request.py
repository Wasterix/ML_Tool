

import functions as fn
import nest_asyncio
nest_asyncio.apply()

#These have already been imported in functions.py. Re-imported them here to show during the webinar.

# Other libraries used
import os

# for converting the frames into bytes
import cv2 

# and for processing arrays   
import numpy as np

# for encoding and decoding Custom Vision predictions 
import json

# for converting the Custom Vision predictions to dataframe   
import pandas as pd

# import async packages
import asyncio
import aiohttp

# for file name pattern matching   
import fnmatch  

# for displaying images from the processes output video   
import matplotlib.pyplot as plt

# importing other required libraries
import random
import textwrap
import datetime 
from PIL import Image
import time 

#These have already been declared in functions.py. Declared them here to show during the webinar.

FACE_MASK_END_POINT = "https://customvision128-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/18b9f548-6d40-414e-bb6f-52f9ddb12344/detect/iterations/Iteration1/image"
FACE_MASK_PREDICTION_KEY = "c78a0bdcf9c44619978e659c1d9d0968"
CONTENT_TYPE = "application/octet-stream"

# web service end-point for the Custom Vision model    
# we will process video frames (which are images)   
POST_URL = "Your custom vision endpoint"

# providing prediction key
HEADERS = {'Prediction-Key': "Your custom vision prediction key", "Content-Type":"application/json"}

# number of API calls per pool of request   
MAX_CONNECTIONS = 100 

# initializing the height and width for frames in the video 
WIDTH = 0
HEIGHT = 0

# creating Output and Stats directories for saving processed videos 
if not os.path.isdir("Output"):
    os.mkdir("Output")
if not os.path.isdir("Stats"):
    os.mkdir("Stats")

# converting raw input video to processed video complete with tags and stats
threshold=0.3
fn.ConvertVideo("input/input_video.mov", "Output/output_video.mp4", threshold, nframes=70)

# TODO: Convert raw input image to processed image complete with tags and stats

# saving processed video as images inside the frames directory
images = []
byteImages = []
vidObj = cv2.VideoCapture("Output/output_video.mp4")
count = 0
success = 1
currentDir = os.getcwd()
if not os.path.isdir("frames"):
    os.mkdir("frames")
while success:
      success, image = vidObj.read()
      if success:
            cv2.imwrite("frames/frame%d.jpg" % count, image) 
            count += 1

images_num=(len(fnmatch.filter(os.listdir(os.getcwd() + "/frames"), '*.jpg')))

# displaying images from frames directory
i=0
for i in range(images_num):
    if i%75==0:
        a = plt.imread("frames/frame%d.jpg" % i)
        plt.imshow(a)
        plt.show()