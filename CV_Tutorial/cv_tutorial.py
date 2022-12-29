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
publish_iteration_name = "Iteration1"

# Authentifizieren des Clients
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Create a new project
print ("Creating project...")
# project_name = uuid.uuid4()
project_name = "quickstart_tutorial"
project = trainer.create_project(project_name)

# Make two tags in the new project
hemlock_tag = trainer.create_tag(project.id, "Hemlock")
cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")

# Hochladen und Kennzeichnen von Bildern
base_image_location = os.path.join(os.path.dirname(__file__), "Images")

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
start_time = time.time()
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 60 sec...")
    time.sleep(60)

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