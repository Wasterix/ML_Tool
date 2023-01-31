import requests
import json
import os
import glob
import time
import pandas as pd
import numpy as np

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

data = {'File in jpg.': [], 'Ground Truth': [], 'Prob_01_Basic': [], 'Prob_02_Pure': []} 

result = pd.DataFrame(data, columns=['File', 'Ground Truth', 'Probability_01_Basic', 'Probability_02_Pure'])


bad_requests = []
i = 1
t = 1
for image_path in image_paths: 
    print()
    print("Gerätnummer:", i)
    print(image_path)
    image_path_last = image_path.split('/')[-1]
    image_path_last = image_path_last.split('.')[0]

    start_time = time.time()
    r =requests.post(url,data=open(image_path,"rb"),headers=headers)

    # Laden des Json Objects als Python Object
    python_object = json.loads(r.content)
    #print(python_object)

    df = pd.DataFrame(python_object['predictions'])
    df = df.drop(columns="tagId")
    df = df.reindex(columns=['tagName', 'probability'])

    #m = df['01_Basic']
    m = df.loc[df['tagName'] == '01_Basic']
    m = m.iloc[0,1]
    n = df.loc[df['tagName'] == '02_Pure']
    n = n.iloc[0,1]

    result.loc[len(result.index)] = [image_path_last, ' - ', m, n]
    #print(result)

    # Extrahieren der Wahrscheinlichkeiten für Basic und Pure aus dem Python Object
    # TODO: Fehlermeldung
    try: 
        python_predictions = python_object["predictions"]
    except:
        print("bad request: ", image_path)
        t = t+1
        bad_requests.append(image_path)
    py_pred_01 = python_predictions[0]
    py_pred_02 = python_predictions[1]

    #print("Vorhersage für: ", image_path)
    #print("Response: ", r.content)
    #print(py_pred_01["tagName"], "hat Wahrscheinlichkeit", round(py_pred_01["probability"], 2))
    #print(py_pred_02["tagName"], "hat Wahrscheinlichkeit", round(py_pred_02["probability"], 2))
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
    #print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))
    
    
    i = i+1
    print()
print(result)
print()
result = result.round(2)
print(result)
print("Anzahl Basic im Test: ", counter_01)
print("Anzahl Pure im Test: ", counter_02)
print("Anzahl bad Requests: ", t-1)
print("List of bad Requests: ", bad_requests)

