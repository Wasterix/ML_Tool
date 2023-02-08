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
url="https://boraproductionecognition-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/3394056c-7080-4680-869a-a2eae3160578/classify/iterations/Iteration1/image"
content_type = 'application/octet-stream'
prediction_key = 'e276b7a116934351be446e1d1ec88477'

# Header werden entsprechend festgelegt
headers={'content-type': content_type,'Prediction-Key': prediction_key}

# Überverzeichnis der Testbilder
directory = "test_images"

# Durch Testbilder iterieren
class_paths = sorted([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])

data = {
    "Filename": [],
    "Ground Truth": [],
}
data.update({folder_name: [] for folder_name in class_paths})
data.update({
    "Correct Prediction": [],
    "Prediction Time [s]": []
})
result = pd.DataFrame.from_dict(data)

# iterating the columns

# Erstellen einer Tabelle um REST-Response zu sammeln
#data = {'File': [], 'Ground Truth': [], 'Prob_01_Basic': [], 'Prob_02_Pure': [], 'Correct Prediction': [], 'Prediction Time': []} 
#result = pd.DataFrame(data, columns=['Filename (.jpg)', 'Ground Truth', 'Probability_01_Basic', 'Probability_02_Pure', 'Correct Prediction', 'Prediction Time [s]'])

# Startzeit für messen der Gesamtlauftzeit des Skriptes
start_time_01 = time.time()

# Festlegen des Grenzwertes für "richtige" Prediction
threshold = 0.4

# Laufvariable für Gerätenummer Index
i = 1

# Es sollen nacheinander alle Testbilder der verschiedenen Ordner (Produktlinien/Modelle/Konfigurationen) durchlaufen werden
for folder_path in class_paths:
    #TODO: Wenn in Dateinamen Punkt vor kommt, zum Beispiel "Professional_3.0.jpg", dann wird das nicht erkannt
    image_paths = glob.glob(os.path.join(directory,folder_path, "*.jpg"))
    image_paths += glob.glob(os.path.join(directory,folder_path, "*.png"))

    # Bestimmen der Ground_Truth um später die Prediction zu prüfen
    ground_truth = folder_path.split('/')[-1]
    bad_requests = []

    # Laufvariable für Zählen von Bad Requests
    bad = 0
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

        try: 
            df = pd.DataFrame(python_object['predictions'])
        except:
            print('oha', i)
        
        try:
            df = df.drop(columns="tagId")
        except:
            print('oha', i)
        
        df = df.reindex(columns=['tagName', 'probability'])

        tags = ['01_s_pure', '02_x_pure', '03_pure', '04_gp4', '05_basic', '06_classic20', '07_pro3']
        m = [df.loc[df['tagName'] == tag].iloc[0,1] for tag in tags]
        
        pred = False

        for m_val, tag in zip(m, tags):
            if m_val > threshold and ground_truth == tag:
                pred = True
                break

        end_time = time.time()
        elapsed_time = end_time - start_time

        #print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))
        result.loc[len(result.index)] = [image_path_last, ground_truth, *m, pred, elapsed_time]

        # Extrahieren der Wahrscheinlichkeiten für Basic und Pure aus dem Python Object
        # TODO: Fehlermeldung
        try: 
            python_predictions = python_object["predictions"]
        except:
            #print("bad request: ", image_path)
            bad = bad+1
            bad_requests.append(image_path)
        py_pred_01 = python_predictions[0]
        py_pred_02 = python_predictions[1]

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
print()
print('Threshold:', threshold)
print("Anzahl bad Requests:", bad)
print("List of bad Requests:", bad_requests)

end_time_02 = time.time()
elapsed_time_02 = end_time_02 - start_time_01
print('Time Total:', elapsed_time_02)

year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
filename = 'result_' + str(year)+"_" +str(month)+"_" +str(day)+"_" +str(hour)+"_" +str(min) + ".csv"


result.to_csv(filename, index=False)

#TODO: If = bla main (chatbot fragen)
