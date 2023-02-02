import requests
import json
import os
import glob
import time
import pandas as pd
import time

# 1. Produktlinie (Kompakt, Modular, Ofen, Multischublade, Kühlschrank)
# 2. Modell (Basic, Pure, XBo .. etc)
# 3. Konfiguration (Tepan, Induktion...)

# Lege fest, welches Modell für die Vorhersage verwendet wird
# Wo bekommt man die Infos für Prediction API her?
# 1. Auf CustomVision Projekt auswählen
# 2. Reiter "Performance"
# 3. "Prediction URL" auswählen
# 4. Unter "If you have image file" folgendes raussuchen
#       url             = Inhalt in Box
#       content-type    = Inhalt rechts von "Content-Type"
#       Prediction-Key  = Inhalt rechts von "Prediction-Key"
url="https://customvision128-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/839631ab-2f69-48ad-8862-f19a66b642e4/classify/iterations/Iteration3/image"
content_type = 'application/octet-stream'
prediction_key = 'c78a0bdcf9c44619978e659c1d9d0968'

# Header werden entsprechend festgelegt
headers={'content-type': content_type,'Prediction-Key': prediction_key}


# Erstellen einer Tabelle um REST-Response zu sammeln (Mit)
data = {'File': [], 'Ground Truth': [], 'Prob_01_Basic': [], 'Prob_02_Pure': [], 'Correct Prediction': [], 'Prediction Time': []} 
result = pd.DataFrame(data, columns=['Filename (.jpg)', 'Ground Truth', 'Probability_01_Basic', 'Probability_02_Pure', 'Correct Prediction', 'Prediction Time [s]'])

# Ordner für Testbilder
folder_paths = ['Images/01_basic', 'Images/02_pure']

# Startzeit für messen der Gesamtlauftzeit des Skriptes
start_time_01 = time.time()

# Festlegen des Grenzwertes für "richtige" Prediction
threshold = 0.9

# Laufvariable für Gerätenummer Index
i = 1

# Es sollen nacheinander alle Testbilder der verschiedenen Ordner (Produktlinien/Modelle/Konfigurationen) durchlaufen werden
# 
for folder_path in folder_paths:
    image_paths = glob.glob(os.path.join(folder_path, "*.jpg"))
    ground_truth = folder_path.split('/')[-1]
    bad_requests = []


    t = 0
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

        try: 
            df = pd.DataFrame(python_object['predictions'])
        except:
            print('oha', i)
        
        try:
            df = df.drop(columns="tagId")
        except:
            print('oha', i)
        
        df = df.reindex(columns=['tagName', 'probability'])

        #m = df['01_Basic']
        m = df.loc[df['tagName'] == '01_Basic']
        m = m.iloc[0,1]
        n = df.loc[df['tagName'] == '02_Pure']
        n = n.iloc[0,1]

        pred = bool
        #print(ground_truth)
        #print(m)
        #print(n)
        #print(pred)

        if m > threshold and m > n and ground_truth == '01_basic':
            pred = True
        elif n > threshold and m < n and ground_truth == '02_pure':
            pred = True
        else:
            pred = False

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))

        #print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))
        result.loc[len(result.index)] = [image_path_last, ground_truth, m, n, pred, elapsed_time]
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



        if py_pred_01["probability"] > threshold:
            print("Glückwunsch, Sie haben ein", py_pred_01["tagName"], "!!")
        else:
            print("Prediction nicht durchführbar -.- \nBitte neues Photo oder manuelle Registrierung.")
        
        i = i+1
        print()


print(result)
print()
result = result.round(2)
print(result)
print("Anzahl bad Requests:", t)
print("List of bad Requests:", bad_requests)

end_time_02 = time.time()
elapsed_time_02 = end_time_02 - start_time_01
print('Time Total:', elapsed_time_02)

year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
filename = 'result_' + str(year)+"_" +str(month)+"_" +str(day)+"_" +str(hour)+"_" +str(min) + ".csv"
result.to_csv(filename, index=False)
