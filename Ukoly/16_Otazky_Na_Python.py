import requests
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/MLTollsStackOverflow.csv")
with open("MLTollsStackOverflow.csv", "wb") as f:
  f.write(r.content)

####################################################################
# Zadání
####################################################################
# Stáhni si soubor MLTollsStackOverflow.csv, který obsahuje počty položených otázek na jednotlivé programovací techniky a další technologie.
# Vyber sloupec python.

# Proveď dekompozici této časové řady pomocí multiplikativního modelu. Dekompozici zobraz jako graf.
df = pd.read_csv("MLTollsStackOverflow.csv")
print(df.head().to_string())
decompose = seasonal_decompose(df['python'], model='additive', period=12)
decompose.plot()
plt.show()

# Vytvoř predikci hodnot časové řady pomocí Holt-Wintersovy metody na 12 měsíců.
# Sezónnost nastav jako 12 a uvažuj multiplikativní model pro trend i sezónnost.
# Výsledek zobraz jako graf.
mod = ExponentialSmoothing(df["python"], seasonal_periods=12, trend="add", seasonal="add", use_boxcox=True, initialization_method="estimated",)
res = mod.fit()
df["HM"] = res.fittedvalues
df[["HM", "python"]].plot()
plt.show()

df_forecast = pd.DataFrame(res.forecast(12), columns=["Prediction"])
df_with_prediction = pd.concat([df, df_forecast])
df_with_prediction[["python", "Prediction"]].plot()
plt.show()