# import requests
#
# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/dopravni-urazy.csv")
# open("dopravni-urazy.csv", "wb").write(r.content)
#
# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kraje.csv")
# open("kraje.csv", "wb").write(r.content)
#
# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/sportoviste.json")
# open("sportoviste.json", "wb").write(r.content)
#
# r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/adopce-zvirat.csv")
# open("adopce-zvirat.csv", "wb").write(r.content)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

urazy = pd.read_csv("dopravni-urazy.csv")
kraje = pd.read_csv("kraje.csv")

# urazy_prumer = pd.DataFrame(columns=["nazev_kraje", "hodnota"])

# for idx, kraj in kraje.iterrows():
#     kod_kraje = kraj["kod_polozky"]
#     nazev_kraje = kraj["nazev_polozky"]
#     prumerna_hodnota = urazy[urazy["kraj"] == kod_kraje]["hodnota"].mean()
#     urazy_prumer = urazy_prumer.append({"nazev_kraje": nazev_kraje, "hodnota": prumerna_hodnota}, ignore_index=True)
#
# print(urazy_prumer)
# urazy_prumer.sort_values(by="hodnota").plot.bar(x="nazev_kraje", y="hodnota", title="Prumer dopravnich urazu v krajich za roky 1995-2017")
# plt.show()
#
# print(set(urazy["rok"])) #mnozina, nema v sebe duplicity

# for kraj in kraje.itertuples():
#     kod_kraje = kraj.kod_polozky
#     nazev_kraje = kraj.nazev_polozky
#     prumerna_hodnota = urazy[urazy["kraj"] == kod_kraje]["hodnota"].mean()
#     urazy_prumer = urazy_prumer.append({"nazev_kraje": nazev_kraje, "hodnota": prumerna_hodnota}, ignore_index=True)

urazy_s_kraji = urazy.merge(kraje, left_on="kraj", right_on="kod_polozky")
print(urazy_s_kraji.head().to_string())

urazy_s_kraji.groupby("nazev_polozky")["hodnota"].mean().sort_values().plot.bar(x="nazev_polozky", y="hodnota")
plt.show()