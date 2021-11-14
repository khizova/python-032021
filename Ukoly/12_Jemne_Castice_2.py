import requests
import pandas as pd
from scipy.stats import mannwhitneyu

# with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/air_polution_ukol.csv") as r:
#   open("air_polution_ukol.csv", 'w', encoding="utf-8").write(r.text)

####################################################################
# Zadání
####################################################################
# V souboru air_polution_ukol.csv najdeš data o množství jemných částic změřených v ovzduší v jedné plzeňské meteorologické stanici a který jsme již používali v úkolu z druhého týdne.
# Načti dataset a převeď sloupec date (datum měření) na typ datetime.
# Dále pokračuj následujícími kroky:
# Z dat vyber data za leden roku 2019 a 2020.
# Porovnej průměrné množství jemných částic ve vzduchu v těchto dvou měsících pomocí Mann–Whitney U testu.
# Formuluj hypotézy pro oboustranný test (nulovou i alternativní) a napiš je do komentářů v programu.
# Měl(a) bys dospět k výsledku, že p-hodnota testu je 1.1 %.
# Rozhodni, zda bys na hladině významnosti 5 % zamítla nulovou hypotézu. Své rozhodnutí napiš do programu.

castice = pd.read_csv("air_polution_ukol.csv")
castice["date"] = pd.to_datetime(castice["date"])
castice = castice.dropna()

# H0: Průměré množství jemných částic v lednu 2019 a lednu 2020 je stejné.
# H1: Průměré množství jemných částic v lednu 2019 a lednu 2020 je různé.

x = castice[(castice["date"].dt.year == 2019) & (castice["date"].dt.month == 1)]["pm25"]
y = castice[(castice["date"].dt.year == 2020) & (castice["date"].dt.month == 1)]["pm25"]
print(mannwhitneyu(x, y))

print("Při hladině významnosti 5% nulovou hypotézu zamítáme.")