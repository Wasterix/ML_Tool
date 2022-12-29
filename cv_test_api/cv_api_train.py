from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
from PIL import Image
import glob

# Replace with valid values
# Endpoint: https://customvision128.cognitiveservices.azure.com/
# Key: 8649c3d4af7347ee8773ba3365edab6b
# Ressource ID: subscriptions/5d4a60e4-3543-43ac-8f31-74b37096d580/resourceGroups/IoT-Backend/providers/Microsoft.CognitiveServices/accounts/CustomVision128

""" ENDPOINT = "PASTE_YOUR_CUSTOM_VISION_TRAINING_ENDPOINT_HERE"
training_key = "PASTE_YOUR_CUSTOM_VISION_TRAINING_SUBSCRIPTION_KEY_HERE"
prediction_key = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_SUBSCRIPTION_KEY_HERE"
prediction_resource_id = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_RESOURCE_ID_HERE" """


ENDPOINT = "https://customvision128.cognitiveservices.azure.com/"
training_key = "8649c3d4af7347ee8773ba3365edab6b"
prediction_key = "c78a0bdcf9c44619978e659c1d9d0968"
prediction_resource_id = "/subscriptions/5d4a60e4-3543-43ac-8f31-74b37096d580/resourceGroups/IoT-Backend/providers/Microsoft.CognitiveServices/accounts/CustomVision128"
publish_iteration_name = "test"
content_type = "application/octet-stream"

# Authentifizieren des Clients
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)


# Create a new project
print ("Creating project...")
#project_name = uuid.uuid4()
project_name = "cv_test_api"
project = trainer.create_project(project_name)

# Make two tags in the new project
basic_tag = trainer.create_tag(project.id, "01_basic")
pure_tag = trainer.create_tag(project.id, "02_pure")

# Hochladen und Kennzeichnen von Bildern
base_image_location = os.path.join(os.path.dirname(__file__), "Images")


print("Adding images...")

image_list = []

from os import walk
from pathlib import Path


for image_num in range(0, 5):
    #file_name = "hemlock_{}.jpg".format(image_num)
    folder_path_source = Path('./Images/01_basic')
    path, dirs, files = next(walk(folder_path_source))

    with open(os.path.join (base_image_location, "01_basic", files[image_num]), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=files[image_num], contents=image_contents.read(), tag_ids=[basic_tag.id]))


for image_num in range(0, 5):
    folder_path_source = Path('./Images/02_pure')
    path, dirs, files = next(walk(folder_path_source))

    with open(os.path.join (base_image_location, "02_pure", files[image_num]), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=files[image_num], contents=image_contents.read(), tag_ids=[pure_tag.id]))

# TODO: Warum kann nur 5 Bilder pro Klasse hochladen?
upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)

# Trainieren des Projektes
print ("Training...")
start_time = time.time()
iteration = trainer.train_project(project.id)


while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 20 sec...")
    time.sleep(20)

# Veröffentlichen der aktuellen Iteration
# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
training_time = round((time.time() - start_time), 1)
print("Training Time: %.1f Seconds" % (training_time))
convert = time.strftime("%M:%S", time.gmtime(training_time))
print("Training Time: ", convert)
print ("Done!")

# Testen des Vorhersageendpunktes
# Now there is a trained endpoint that can be used to make a prediction
#prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key, "Content-Type": content_type})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)


with open(os.path.join (base_image_location, "Test/IMG20220223145924_02.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))

# rüger flo
# erbe sebastian (serbe) -> ki mensch bei bora
# Ausführen der Anwendung
# in Konsole python CustomVisionQuickstart.py