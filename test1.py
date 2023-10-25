import pandas as pd

df_81A = pd.read_csv('81A.txt', sep='\t')
df_26A = pd.read_csv("26A.txt", sep="\t")

for col in df_81A.columns:
    print(col)
    