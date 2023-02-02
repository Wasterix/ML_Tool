import pandas as pd

df = pd.read_csv('result.csv')
df.to_excel('result.xls', index=False)
print(df.to_string())

#print(df)
