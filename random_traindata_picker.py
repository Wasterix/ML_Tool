import os
import random
from pathlib import Path
import shutil

#####################################################################################################################
# Diese Funktion kopiert eine bestimmte Anzahl Trainingsdaten aus dem Ordner Experiment_02 -> traindata_complete    #
# in die richtigen Ordner für die Trainingsdaten                                                                 #   
#                                                                                                                   #   
#                                                                                                                   #
#           Für Experiment 2!!!!                                                                                    #
#                                                                                                                   #
# Wichtig:  Die Namen der Ordner sind in der Liste "products" anzugeben und müssen identisch zu den Ordnern sein.   #
#           Bei "ratio" wird der Anteil der Trainingsdaten in Prozent angegeben                                     #
#           Richtige Konfiguration bei "shutil.copy" oder "shutil.move" wählen                                      #
##################################################################################################################### 

products = ["01_Basic", "02_Pure"]

os.mkdir('./datasplit/01_train')

source = './Experiment_02/traindata_complete/'
target = './datasplit/'

# Seed fixieren Wählt immer die gleichen Photos zufällig aus (Reproduzierbarkeit)
random.seed(42)

for i in products: 

    os.mkdir('./datasplit/01_train/' + i)   
    
    # Pfad von Source-Daten und Zieldaten
    folder_path_source = Path(source + i)         
    target_path_train = Path(target  + "01_train/" + i)
    #target_path_test = Path(target + "02_test/" + i)

    # Speichern von Pfad, Ordner und Dateien in Variablen (path, dirs, files)
    source_file = os.walk(folder_path_source)
    print("Fehler: ", source_file)
    
    path, dirs, files = next(source_file)
    file_count = len(files)

    # Wähle bestimmte Anzahl an Trainingsdaten
    train_data_num = 200            # weil das 80 Prozent der Bilder des Basic sind (Basic -> 510, Pure -> 592)
    #test_data_num = file_count - train_data_num
    
    # Wähle zufällige Trainingsdaten, mit bestimmter Anzahl
    train_files_random = random.sample(files, len(files))
    
    # Sortiere die ersten n Daten in Trainingsdaten und den Rest in Testdaten
    for k in range(0, train_data_num):
        
        source_file = str(folder_path_source) + "/" + str(train_files_random[k])
        target_file = str(target_path_train) + "/" + str(train_files_random[k])
        
        #shutil.move(source_file, target_file)
        #shutil.copy(source_file, target_file)
    