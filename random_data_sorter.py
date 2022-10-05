import os
import random
from pathlib import Path
import shutil
from datetime import datetime

#####################################################################################################################
# Diese Funktion sortiert Dateien aus dem Ordner all_data in die Ordner Testdaten und Trainingsdaten um             #   
#                                                                                                                   #
# Wichtig:  Die Namen der Ordner sind in der Liste "products" anzugeben und müssen identisch zu den Ordnern sein.   #
#           Bei "ratio" wird der Anteil der Trainingsdaten in Prozent angegeben                                     #
#           Richtige Konfiguration bei "shutil.copy" oder "shutil.move" wählen                                      #
##################################################################################################################### 

timestamp = datetime.now()

products = ["01 Basic", "02 Pure", "03 S Pure", "04 X Pure", "05 GP4"]

os.mkdir('./datasplit')
os.mkdir('./datasplit/01_train')
os.mkdir('./datasplit/02_test' )



source = './051 Photos original no split/'
target = './datasplit/'

# Wählt immer die gleichen Photos zufällig aus
random.seed(42)

for i in products: 

    os.mkdir('./datasplit/01_train/' + i)   
    os.mkdir('./datasplit/02_test/' + i)
    
    # Pfad von Source-Daten und Zieldaten
    folder_path_source = Path(source + i)         
    target_path_train = Path(target  + "01_train/" + i)
    target_path_test = Path(target + "02_test/" + i)

    # Speichern von Pfad, Ordner und Dateien in Variablen (path, dirs, files)
    path_file = os.walk(folder_path_source)

    
    path, dirs, files = next(path_file)
    file_count = len(files)

    """     # Wähle Prozentsatz der Trainingsdaten, Rest sind Testdaten
    ratio = 70             
    ratio = ratio/100 
    train_data_num = math.ceil(ratio*file_count) """

    # Wähle bestimmte Anzahl an Trainingsdaten
    train_data_num = 50
    test_data_num = file_count - train_data_num
    
    # Wähle zufällige Trainingsdaten, mit bestimmter Anzahl
    train_files_random = random.sample(files, len(files))
    
    # Sortiere die ersten n Daten in Trainingsdaten und den Rest in Testdaten
    for k in range(0, file_count):
        if k < train_data_num:
            source_file = str(folder_path_source) + "/" + str(train_files_random[k])
            target_file = str(target_path_train) + "/" + str(train_files_random[k])

            shutil.move(source_file, target_file)
            #shutil.copy(source, target)
        else:
            source_file = str(folder_path_source) + "/" + str(train_files_random[k])
            target_file2 = str(target_path_test) + "/" + str(train_files_random[k])

            shutil.move(source_file, target_file2)
