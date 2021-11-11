
import requests

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/AirPassengers.csv")
with open("AirPassengers.csv", "wb") as f:
  f.write(r.content)

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/PJME_daily.csv")
with open("PJME_daily.csv", "wb") as f:
  f.write(r.content)

  import pandas
  import matplotlib.pyplot as plt

  df = pandas.read_csv("AirPassengers.csv")
  df = df.rename({"#Passengers": "Passengers"}, axis=1)
  df = df.set_index("Month")
  df.plot()

  from statsmodels.tsa.holtwinters import ExponentialSmoothing

  mod = ExponentialSmoothing(df["Passengers"], seasonal_periods=12, trend="add", seasonal="add", use_boxcox=True,
                             initialization_method="estimated", )
  res = mod.fit()
  df["HM"] = res.fittedvalues
  df[["HM", "Passengers"]].plot()

  from statsmodels.graphics.tsaplots import plot_acf

  plot_acf(df["Passengers"])
  plt.show()