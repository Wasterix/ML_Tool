from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
from PIL import Image
import glob

#ENDPOINT = "https://customvision128.cognitiveservices.azure.com/"
prediction_endpoint = "https://customvision128-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/839631ab-2f69-48ad-8862-f19a66b642e4/classify/iterations/Iteration3/image"
prediction_key = "c78a0bdcf9c44619978e659c1d9d0968"
content_type = "application/octet-stream"
#prediction_resource_id = "/subscriptions/5d4a60e4-3543-43ac-8f31-74b37096d580/resourceGroups/IoT-Backend/providers/Microsoft.CognitiveServices/accounts/CustomVision128"
publish_iteration_name = "Iteration3"
project_id = "46cfeccb-1352-46d8-bc91-5712169e6c5e"
#prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key, "Content-Type": content_type})

# Hochladen und Kennzeichnen von Bildern
base_image_location = os.path.join(os.path.dirname(__file__), "Images")


# Testen des Vorhersageendpunktes
# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Content-Type": content_type, "Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

# Wahl und Zuordnung des richtigen Projektes
with open(os.path.join (base_image_location, "Test/IMG20220223145924_02.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project_id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))