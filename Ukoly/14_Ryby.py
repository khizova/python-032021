import requests
import pandas as pd
import statsmodels.formula.api as smf

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/Fish.csv")
with open("Fish.csv", "wb") as f:
  f.write(r.content)

####################################################################
# Zadání
####################################################################
# V souboru Fish.csv najdeš informace o rybách z rybího trhu.
# Vytvoř regresní model, který bude predikovat hmnotnost ryby na základě její diagonální délky (sloupec Length2).
# Zkus přidat do modelu výšku ryby (sloupec Height) a porovnej, jak se zvýšila kvalita modelu.
# Nakonec pomocí metody target encoding zapracuj do modelu živočišný druh ryby.

df = pd.read_csv("Fish.csv")
print(df.head(n=10).to_string())

mod1 = smf.ols(formula="Weight ~ Length2", data=df)
res1 = mod1.fit()
print(res1.summary())

mod2 = smf.ols(formula="Weight ~ Length2 + Height", data=df)
res2 = mod2.fit()
print(res2.summary())

print("Přidáním výšky ryby do regresního modelu se zvýšila jeho kvalita o cca 3,7%.")

####################################################################
# Target / One hot encoding
####################################################################

one_hot_encoding = pd.get_dummies(df["Species"], prefix="Species")
df2 = df.join(one_hot_encoding)
# print(df.head().to_string())

mod3 = smf.ols(formula="Weight ~ Length2 + Height + Species_Bream + Species_Parkki +"
                       "Species_Perch + Species_Pike + Species_Roach + Species_Smelt + Species_Whitefish", data=df2)
res3 = mod3.fit()
print(res3.summary())

mean = df.groupby("Species")["Weight"].mean()
df["weight_species_mean"] = df["Species"].map(mean)
# print(df.head().to_string())

mod4 = smf.ols(formula="Weight ~ Length2 + Height + weight_species_mean", data=df)
res4 = mod4.fit()
print(res4.summary())