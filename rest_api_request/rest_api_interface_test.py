# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os 
from pprint import pprint
import requests

'''
This sample makes a call to the Computer Vision API with a URL image query to analyze an image,
and then returns user input parameter data like category, description, and color.
API: https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/587f2c6a154055056008f200
'''

test_end_point = "https://customvision128.cognitiveservices.azure.com/"
test_subscription_key = "8649c3d4af7347ee8773ba3365edab6b"
test_prediction_key = "c78a0bdcf9c44619978e659c1d9d0968"

subscription_key = test_subscription_key
endpoint = test_end_point


""" # Add your Computer Vision subscription key and endpoint to your environment variables.
subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
endpoint = os.environ[test_end_point] + "/vision/v2.1/analyze" """

# Request headers.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters. All of them are optional.
params = {
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
}

# Any image with objects will work.
body = {'url': 'https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg'}

# Call the API.
try:
    response = requests.post(endpoint, headers=headers, params=params, json=body)
    response.raise_for_status()

    print("\nHeaders:\n")
    print(response.headers)

    print("\nJSON Response:\n")
    pprint(response.json())
except Exception as ex:
    raise ex





""" 

######################
# ab hier anderes Tutorial
#These have already been declared in functions.py. Declared them here to show during the webinar.

# web service end-point for the Custom Vision model    
# we will process video frames (which are images)   
POST_URL = test_end_point

# providing prediction key
HEADERS = {'Prediction-Key': "Your custom vision prediction key", "Content-Type":"application/json"}

# number of API calls per pool of request   
MAX_CONNECTIONS = 100 

# initializing the height and width for frames in the video 
WIDTH = 0
HEIGHT = 0
# da anderes Tutorial aus
############# """