import os
import random
from pathlib import Path
import shutil
from datetime import datetime

#####################################################################################################################
# Diese Funktion sortiert Dateien aus dem Ordner all_data in die Ordner Testdaten und Trainingsdaten um             #   
#                
# 
#           Für Experiment 2!!!!
#                                                                                                                   #
# Wichtig:  Die Namen der Ordner sind in der Liste "products" anzugeben und müssen identisch zu den Ordnern sein.   #
#           Bei "ratio" wird der Anteil der Trainingsdaten in Prozent angegeben                                     #
#           Richtige Konfiguration bei "shutil.copy" oder "shutil.move" wählen                                      #
##################################################################################################################### 

timestamp = datetime.now()

products = ["01_Basic", "02_Pure"]

os.mkdir('./datasplit')
os.mkdir('./datasplit/01_train')
os.mkdir('./datasplit/02_test' )



source = './Experiment_02/011_no_split/'
target = './datasplit/'


print("Start")

# Wählt immer die gleichen Photos zufällig aus
random.seed(42)

for i in products: 

    os.mkdir('./datasplit/01_train/' + i)   
    os.mkdir('./datasplit/02_test/' + i)
    
    # Pfad von Source-Daten und Zieldaten
    folder_path_source = Path(source + i)         
    target_path_train = Path(target  + "01_train/" + i)
    target_path_test = Path(target + "02_test/" + i)

    print(i,"Start!!!")
    # Speichern von Pfad, Ordner und Dateien in Variablen (path, dirs, files)
    fehler = os.walk(folder_path_source)
    #print("Fehler: ", fehler)
    
    path, dirs, files = next(fehler)
    file_count = len(files)

    """     # Wähle Prozentsatz der Trainingsdaten, Rest sind Testdaten
    ratio = 70             
    ratio = ratio/100 
    train_data_num = math.ceil(ratio*file_count) """

    # Wähle bestimmte Anzahl an Trainingsdaten
    train_data_num = 408            # weil das 80 Prozent der Bilder des Basic sind (Basic -> 510, Pure -> 592)
    test_data_num = file_count - train_data_num
    
    # Wähle zufällige Trainingsdaten, mit bestimmter Anzahl
    train_files_random = random.sample(files, len(files))
    
    # Sortiere die ersten n Daten in Trainingsdaten und den Rest in Testdaten
    for k in range(0, file_count):
        if k < train_data_num:
            source_file = str(folder_path_source) + "/" + str(train_files_random[k])
            target_file = str(target_path_train) + "/" + str(train_files_random[k])
            print("Source:", source_file)
            print("Target:", target_file)

            
            shutil.move(source_file, target_file)
            #shutil.copy(source, target)
        else:
            source_file = str(folder_path_source) + "/" + str(train_files_random[k])
            target_file2 = str(target_path_test) + "/" + str(train_files_random[k])
            #print("Source:", source)
            #print("Target2:", target)
            shutil.move(source_file, target_file2)
            #shutil.copy(source, target2)  
    print(i,"Ready!!!") 
    
print("end")