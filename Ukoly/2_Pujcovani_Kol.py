import requests
import pandas as pd
import numpy as np

# r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/london_merged.csv")
# open("london_merged.csv", 'wb').write(r.content)

# V souboru london_merged.csv najdeš informace o počtu vypůjčení jízdních kol v Londýně.
# Vytvoř sloupec, do kterého z časové značky (sloupec timestamp) ulož rok.
# Vytvoř kontingenční tabulku, která porovná kód počasí (sloupec weather_code se sloupcem udávající rok.
# Definice jednotlivých kódů jsou:
#
# 1 = Clear ; mostly clear but have some values with haze/fog/patches of fog/ fog in vicinity
# 2 = scattered clouds / few clouds
# 3 = Broken clouds
# 4 = Cloudy
# 7 = Rain/ light Rain shower/ Light rain
# 10 = rain with thunderstorm
# 26 = snowfall
# 94 = Freezing Fog

london = pd.read_csv("london_merged.csv")
# print(london.dtypes)
# print(london.columns)

london["year"] = pd.to_datetime(london["timestamp"]).dt.year
print(london.head().to_string())

london["weather"] = np.where(london["weather_code"] == 1.0, "1.0 - Clear",
                    np.where(london["weather_code"] == 2.0, "2.0 - Scattered clouds / few clouds",
                    np.where(london["weather_code"] == 3.0, "3.0 - Broken clouds",
                    np.where(london["weather_code"] == 4.0, "4.0 - Cloudy",
                    np.where(london["weather_code"] == 7.0, "7.0 - Rain/ light Rain shower/ Light rain",
                    np.where(london["weather_code"] == 10.0, "10.0 - Rain with thunderstorm",
                    np.where(london["weather_code"] == 26.0, "26.0 - Snowfall", "94.0 - Freezing Fog")))))))
print(london.head().to_string())

london_pivot = pd.pivot_table(london, index="weather", columns="year", values="cnt", aggfunc=np.sum, margins=True)
print("Počet jízd pro jednotlivé kódy počasí v roce: \n", london_pivot.to_string())

# Rozšířené zadání
# Jako hodnoty v kontingenční tabulce zobraz relativní počty jízd pro jednotlivé kódy počasí v jednom roce.
# Příklad možného výsledku by byl: v roce 2020 proběhlo 40 % jízd za počasí s kódem 1, 20 % jízd za počasí s kódem 2 a 40 % jízd za počasí s kódem 3 atd.

london_pivot_percentage = london_pivot.div(london_pivot.iloc[-1,:], axis=1)
print("Relativní počet jízd pro jednotlivé kódy počasí v roce: \n", london_pivot_percentage.to_string())


