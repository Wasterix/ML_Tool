import pandas as pd
import numpy as np
import shutil
import os

#####################################################################################################################
# Diese Funktion liest Filenamen ein, die in einer Excel-Datei gespeichert wurden                                   #   
# Anschließend werden Ordner erstellt in den, die entsprechenden Files sortiert werden                              #   
#                                                                                                                   #
# Diese Funktion ist entstanden um eine identische Liste von ausgewählten Testdaten wieder herzustellen             #
##################################################################################################################### 


# Lies aus Excel Datei Namen aller Files ein
df = pd.read_excel(r'./Testdaten_Experiment2.xlsx')

# Übergebe Spalten in Listen
basic_test_list = df.loc[:, ["Basic"]]
pure_test_list = df.loc[:, ["Pure"]]

# Wandle Liste in Array um
btl = basic_test_list.to_numpy()
ptl = pure_test_list.to_numpy()

# Erzeuge neue Ordner
os.mkdir('./test/btl')
os.mkdir('./test/ptl')

# Verschiebe gewählte Testdaten in neuen Ordner für Basic
for i in btl:
    source_file = "./Experiment_02/Rohdaten/basic_niederndorf" + "/" + str(i[0])
    target_file = "./test/btl" + "/" + str(i[0])
    shutil.move(source_file, target_file)

# Verschiebe gewählte Testdaten in neuen Ordner für Pure
for i in ptl:
    source_file = "./Experiment_02/Rohdaten/pure_raubling" + "/" + str(i[0])
    target_file = "./test/ptl" + "/" + str(i[0])
    shutil.move(source_file, target_file)











