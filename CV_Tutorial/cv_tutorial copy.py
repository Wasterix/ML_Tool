from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

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
prediction_key = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_SUBSCRIPTION_KEY_HERE"
prediction_resource_id = "/subscriptions/5d4a60e4-3543-43ac-8f31-74b37096d580/resourceGroups/IoT-Backend/providers/Microsoft.CognitiveServices/accounts/CustomVision128"

# Authentifizieren des Clients
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Erstellen eines neuen Custom Vision-Projektes
publish_iteration_name = "Iteration 1"

# Create a new project
print ("Creating project...")
# project_name = uuid.uuid4()
project_name = "quickstart_tutorial"
project = trainer.create_project(project_name)

# Hinzufügen Tags zu Projekt
# Make two tags in the new project
hemlock_tag = trainer.create_tag(project.id, "Hemlock")
cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")

path_Hemlock = "/home/wasterix/VS_Code/CV_Tutorial/Images/Hemlock"
path_japanese_cherry = "/home/wasterix/VS_Code/CV_Tutorial/Images/Japanese_Cherry"

hemlock_images_list = os.listdir(path_Hemlock)
japanese_Cherry_images_list = os.listdir(path_japanese_cherry)

print(hemlock_images_list)

print("Adding images...")

for image_num in hemlock_images_list:
    file_name = "CV_Tutorial/Images/Hemlock/" + image_num
    with open(file_name, mode ="rb") as image_contents:
        trainer.create_images_from_files(project.id, images=[ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[hemlock_tag.id])])
exit()
for image_num in japanese_Cherry_images_list:
    file_name = "Images/Japanese_Cherry/" + image_num
    with open(file_name, mode="rb") as image_contents:
        trainer.create_images_from_files(project.id, images=[ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[japanese_cherry_tag.id])])

print("Training... ")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training Status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Make it the default project endpoint
trainer.update_iteration(project.id, iteration.id, is_default=True)
print ("Done!")

""" 

# Hochladen und Kennzeichnen von Bildern
base_image_location = os.path.join (os.path.dirname(__file__), "Images")

print("Adding images...")

image_list = []

for image_num in range(1, 11):
    file_name = "hemlock_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, "Hemlock", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[hemlock_tag.id]))

for image_num in range(1, 11):
    file_name = "japanese_cherry_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, "Japanese_Cherry", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[cherry_tag.id]))

upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)

# Trainieren des Projektes
print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 20 seconds...")
    time.sleep(20)

# Veröffentlichen der aktuellen Iteration
# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")
 
# Testen des Vorhersageendpunktes
# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

with open(os.path.join (base_image_location, "Test/test_image.jpg"), "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))


# Ausführen der Anwendung
# in Konsole python CustomVisionQuickstart.py 
# 
# """