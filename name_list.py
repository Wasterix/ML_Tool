import os
import csv

#####################################################################################################################
#                                                                                                                   #
# Diese Funktion erstellt eine Liste aller Dateien eines Ordners Ordners Test                                                #   
#           Sie wurde geschrieben, um eine Liste von Testdaten dokumentarisch festzuhalten                          #
#           Dies gewährleistet Reproduzierbarkeit und Verlgeichbarkeit verschiedener Experimente                    #
#                                                                                                                   #
##################################################################################################################### 

# Angabe des Ordnerpfades
source_01_Basic = "./Experiment_02/007_Testset/02_test/01_Basic"
source_02_Pure ="./Experiment_02/007_Testset/02_test/02_Pure"

# Erstellen der Listen
list_01_basic_test = []
list_02_pure_test = []

# Ziehen der Filenamen aus Durchlauf durch Ordner
_, _, files_basic = next(os.walk(source_01_Basic))
_, _, files_pure = next(os.walk(source_02_Pure))

# Letztes File an Liste anhängen
list_01_basic_test.append(files_basic)
list_02_pure_test.append(files_pure)

# Ausgabe der Länge der Liste
print(len(list_01_basic_test))
print(len(list_02_pure_test))

# Ausgabe der Liste
print("Basic:", list_01_basic_test)
print("Pure:", list_02_pure_test)

