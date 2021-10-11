import requests
import pandas as pd
import numpy as np

# with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
#   open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné plzeňské meteorologické stanici.
# Načti dataset a převeď sloupec date (datum měření) na typ datetime.
# Přidej sloupce s rokem a číslem měsíce, které získáš z data měření.
# Vytvoř pivot tabulku s průměrným počtem množství jemných částic (sloupec pm25) v jednotlivých měsících a jednotlivých letech. Jako funkci pro agregaci můžeš použít numpy.mean.

castice = pd.read_csv("air_polution_ukol.csv")
castice["date"] = pd.to_datetime(castice["date"])
castice["rok"] = castice["date"].dt.year
castice["mesic"] = castice["date"].dt.month
# print(castice.head())

# Pivot tabulka s průměrným počtem množství jemných částic (sloupec pm25) v jednotlivých měsících a jednotlivých letech.
castice_pivot = pd.pivot_table(castice, index="mesic", columns="rok", values="pm25", aggfunc=np.mean, fill_value=0, margins=True)
print(castice_pivot.to_string())

# Dobrovolný doplněk
# Podívej se do první lekce na část o teplotních mapách a zobrat výsledek analýzy jako teplotní mapu.
# Použij metodu dt.dayofweek a přidej si do sloupce den v týdnu. Číslování je od 0, tj. pondělí má číslo 0 a neděle 6.
# Porovnej, jestli se průměrné množství jemných částic liší ve všední dny a o víkendu.

import matplotlib.pyplot as plt
import seaborn as sns

# Heatmap s průměrným počtem množství jemných částic (sloupec pm25) v jednotlivých měsících a jednotlivých letech.
sns.heatmap(castice_pivot, annot=True, fmt=".1f", linewidths=.7)
plt.title("Průměrný počet množství jemných částic v jednotlivých měsících a letech", fontsize=12, pad=15)
plt.show()

# Porovnání průměrného množství jemných částic ve všední dny a o víkendu pomocí tabulky.
castice_rozsirene = castice
castice_rozsirene["day_of_week"] = castice_rozsirene["date"].dt.dayofweek
castice_rozsirene["type_of_day"] = np.where(castice_rozsirene["day_of_week"] <= 4, "working_day", "weekend")
castice_porovnani = castice_rozsirene.groupby(["type_of_day"])["pm25"].mean()
castice_porovnani = pd.DataFrame(castice_porovnani)
castice_porovnani = castice_porovnani.reset_index()
print(castice_rozsirene.head())
print("Porovnání průměrného množství jemných částic ve všední dny a o víkendu: \n", castice_porovnani.to_string(index=False))

# Porovnání průměrného množství jemných částic ve všední dny a o víkendu pomocí grafu.
castice_porovnani.plot.bar(x="type_of_day", y="pm25", legend=None)
plt.title("Porovnání průměrného množství jemných částic ve všední dny a o víkendu", fontsize=12, pad=15)
# plt.legend(["pruměrné množství jemných částic"], loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=3, fancybox=True, shadow=True)
plt.show()