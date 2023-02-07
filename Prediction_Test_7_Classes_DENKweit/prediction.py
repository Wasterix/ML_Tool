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


directory = "test_images"

# Ordner für Testbilder
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
print(result.columns[3])


# Erstellen einer Tabelle um REST-Response zu sammeln
#data = {'File': [], 'Ground Truth': [], 'Prob_01_Basic': [], 'Prob_02_Pure': [], 'Correct Prediction': [], 'Prediction Time': []} 
#result = pd.DataFrame(data, columns=['Filename (.jpg)', 'Ground Truth', 'Probability_01_Basic', 'Probability_02_Pure', 'Correct Prediction', 'Prediction Time [s]'])

# Startzeit für messen der Gesamtlauftzeit des Skriptes
start_time_01 = time.time()

# Festlegen des Grenzwertes für "richtige" Prediction
threshold = 0.9

# Laufvariable für Gerätenummer Index
i = 1

# Es sollen nacheinander alle Testbilder der verschiedenen Ordner (Produktlinien/Modelle/Konfigurationen) durchlaufen werden
# 
for folder_path in class_paths:
    image_paths = glob.glob(os.path.join(directory,folder_path, "*.jpg"))
    image_paths += glob.glob(os.path.join(directory,folder_path, "*.png"))
    #print("Folder_Path:", folder_path)
    #print(image_paths)
    # Bestimmen der Ground_Truth um später die Prediction zu prüfen
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
        #print(r)

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

        """       for product in result.columns[2:9]:
                    print("Wahrscheinlichkeit für Produkt", product, "ist ... Prozent")
                    
                    print(df.loc[df[product] == ground_truth])
                    exit()

                    m01 = df.loc[df[product] == ground_truth]
                    m01 = m01.iloc[0,1]
                    print(m01)

                    if m01 > threshold and ground_truth == product:
                        pred = True
                    else: 
                        pred = False
                    #TODO Peng mit den Wahrscheinlichkeiten füllen
                    peng = []

 
                    
                    print("Ground Truth:", ground_truth)

                    exit()
        result.loc[len(result.index)] = [image_path_last, ground_truth, peng, pred, elapsed_time]
        exit() """
        #m = df['01_Basic']
        #TODO: tagNames anpassen, Positionen für Pandas anpassen
        # 01_s_pure, 02_x_pure, 03_pure, 04_gp4, 05_basic, 06_classic20, 07_pro3


        #print(df)
        m01 = df.loc[df['tagName'] == '01_s_pure']
        m01 = m01.iloc[0,1]
        m02 = df.loc[df['tagName'] == '02_x_pure']
        m02 = m02.iloc[0,1]
        m03 = df.loc[df['tagName'] == '03_pure']
        m03 = m03.iloc[0,1]
        m04 = df.loc[df['tagName'] == '04_gp4']
        m04 = m04.iloc[0,1]
        m05 = df.loc[df['tagName'] == '05_basic']
        m05 = m05.iloc[0,1]
        m06 = df.loc[df['tagName'] == '06_classic20']
        m06 = m06.iloc[0,1]
        m07 = df.loc[df['tagName'] == '07_pro3']
        m07 = m07.iloc[0,1]
        





        """ print(m01)
        print(m02)
        print(m03)
        print(m04)
        print(m05)
        print(m06)
        print(m07) """
      
        
        pred = bool
        #print(ground_truth)
        #print(m)
        #print(n)
        #print(pred)

        if m01 > threshold and m01 > m02 and ground_truth == '01_s_pure':
            pred = True
        elif m01 > threshold and m01 < m02 and ground_truth == '02_x_pure':
            pred = True
        else:
            pred = False

        
        end_time = time.time()
        elapsed_time = end_time - start_time
        #print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))

        #print("Die Vorhersage dauerte {} Sekunden".format(round(elapsed_time,2)))
        result.loc[len(result.index)] = [image_path_last, ground_truth, m01, m02, m03, m04, m05, m06, m07, pred, elapsed_time]
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

#TODO: If = bla main (chatbot fragen)
