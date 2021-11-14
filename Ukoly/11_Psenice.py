import requests
import pandas as pd
from scipy.stats import mannwhitneyu

# with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/psenice.csv") as r:
#   open("psenice.csv", 'w', encoding="utf-8").write(r.text)

####################################################################
# Zadání
####################################################################
# V souboru jsou data o délce zrn pšenice v milimetrech pro dvě odrůdy - Rosa a Canadian.
# Proveď statistický test hypotézy o tom, zda se délka těchto dvou zrn liší.
# K testu použij Mann–Whitney U test, který jsme používali na lekci.
# V komentáři u programu formuluj hypotézy, které budeš ověřovat.
# Je potřeba formulovat dvě hypotézy - nulovou a alternativní.
# Provádíme oboustranný test, takže alternativní hypotézy by měla být, že průměry délky zrna jsou různé (nejsou si rovné).
# Pomocí modulu scipy urči p-hodnotu testu a porovnej ji s hladinou významnosti 5 %.
# V komentáři uveď závěr, jestli nulovou hypotézu na základě p-hodnoty zamítáme.
# Platí pravidlo, že je-li p-hodnota menší než hladina významnosti, nulovou hypotézu zamítáme.
# V opačném případě říkáme, že ji nezamítáme.

df = pd.read_csv("psenice.csv")
print(df.head().to_string())

# H0: Průměry délky zrna jsou si rovné.
# H1: Průměry délky zrna jsou různé (nejsou si rovné).

x = df["Rosa"]
y = df["Canadian"]
print(mannwhitneyu(x, y))

print("Při hladině významnosti 5% nulovou hypotézu zamítáme.")




