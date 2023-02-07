import pandas as pd
from sklearn.metrics import confusion_matrix

# Laden Sie die CSV-Datei in einen Pandas-DataFrame
df = pd.read_csv("result_2023_2_6_15_20.csv")
print(df)

df = df.drop('Prediction Time [s]', axis=1)
df = df.drop('Filename (.jpg)', axis=1)
df = df.drop('Correct Prediction', axis=1)
df = df.drop('Probability_02_Pure', axis=1)

print(df)

df.loc[df["Probability_01_Basic"] >= 0.5, "Probability_01_Basic"] = 1.0
df.loc[df["Probability_01_Basic"] < 0.5, "Probability_01_Basic"] = 0.0

df.loc[df["Ground Truth"] == "01_basic", "Ground Truth"] = 1.0
df.loc[df["Ground Truth"] == "02_pure", "Ground Truth"] = 0.0

df["Ground Truth"] = df["Ground Truth"].astype(int)
df["Probability_01_Basic"] = df["Probability_01_Basic"].astype(int)
print(df.dtypes)


# Extrahieren Sie die beiden Spalten mit den Predictions
y_true = df["Ground Truth"]
y_pred = df["Probability_01_Basic"]

# Berechnen Sie die Konfusionsmatrix
confusion_matrix = confusion_matrix(y_true, y_pred)

# Ausgabe der Konfusionsmatrix
print(confusion_matrix)