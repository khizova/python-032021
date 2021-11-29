import requests
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Concrete_Data_Yeh.csv")
with open("Concrete_Data_Yeh.csv", "wb") as f:
  f.write(r.content)

df = pd.read_csv("Concrete_Data_Yeh.csv")
print(df.head(n=20).to_string())
# print(df.isna().sum())

# sns.heatmap(df.corr(), annot=True, linewidths=.5, fmt=".2f", cmap="Blues", vmax=1)
# plt.show()

mod = smf.ols(formula="csMPa ~ cement + slag + flyash + water + superplasticizer"
                            "+ coarseaggregate + fineaggregate + age", data=df)
res = mod.fit()
print(res.summary())
print("Koeficient determinace je 0.616, co znamená, že modelem vysvětlíme jenom 60% rozptylu hodnot. Model není příliš kvalitní.")
print("Záporný regresní koeficient má voda.")

