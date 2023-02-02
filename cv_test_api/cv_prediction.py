import requests
import json
import os
import glob
import time

# 1. Produktlinie (Kompakt, Modular, Ofen, Multischublade, Kühlschrank)
# 2. Modell (Basic, Pure, XBo .. etc)
# 3. Konfiguration (Tepan, Induktion...)
# Ausgabe 

url="https://customvision128-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/839631ab-2f69-48ad-8862-f19a66b642e4/classify/iterations/Iteration3/image"
headers={'content-type':'application/octet-stream','Prediction-Key':'c78a0bdcf9c44619978e659c1d9d0968'}

folder_path = "Images/Test"
image_paths = glob.glob(os.path.join(folder_path, "*.jpg"))

counter_01 = 0
counter_02 = 0
top_tipp = []
for image_path in image_paths: 
    
    start_time = time.time()
    r =requests.post(url,data=open(image_path,"rb"),headers=headers)

    # Laden des Json Objects als Python Object
    python_object = json.loads(r.content)

    # Extrahieren der Wahrscheinlichkeiten für Basic und Pure aus dem Python Object
    python_predictions = python_object["predictions"]
    py_pred_01 = python_predictions[0]
    py_pred_02 = python_predictions[1]

    print("Vorhersage für: ", image_path)
    #print("Response: ", r.content)
    print(py_pred_01["tagName"], "hat Wahrscheinlichkeit", round(py_pred_01["probability"], 2))
    print(py_pred_02["tagName"], "hat Wahrscheinlichkeit", round(py_pred_02["probability"], 2))
    #print("Probability für Pure: ", round(py_pred_02_pure["probability"], 2))


    if py_pred_01["tagName"] == "01_Basic":
        counter_01 = counter_01 + 1
    elif py_pred_01["tagName"] == "02_Pure":
        counter_02 = counter_02 + 1

    threshold = 0.9
    if py_pred_01["probability"] > threshold:
        print("Glückwunsch, Sie haben ein", py_pred_01["tagName"], "!!")
    else:
        print("Prediction nicht durchführbar -.- \nBitte neues Photo oder manuelle Registrierung.")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))

    print()
print("Anzahl Basic im Test: ", counter_01)
print("Anzahl Pure im Test: ", counter_02)

