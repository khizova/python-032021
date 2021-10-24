import requests
import pandas as pd

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv")
open("lexikon-zvirat.csv", "wb").write(r.content)

####################################################################
# Nacteni dat
####################################################################
# Načti si soubor pomocí metody read_csv. Pozor, tento dataset využívá jako oddělovač středník, nikoliv čárku. Při načítání dat proto nastav parametr sep na znak středníku (";").
# Poslední sloupec a poslední řádek obsahují nulové hodnoty. Zbav se tohoto sloupce a řádku.
# Nastav sloupec id jako index pomocí metody set_index.

lexikon_zvirat = pd.read_csv("lexikon-zvirat.csv", delimiter=";")
lexikon_zvirat = lexikon_zvirat.dropna(how="all", axis="columns")
lexikon_zvirat = lexikon_zvirat.dropna(how="all", axis="rows")
lexikon_zvirat = lexikon_zvirat.set_index(["id"])

####################################################################
# Lexikon zvirat 2
####################################################################
# Chceme ke každému zvířeti vytvořit popisek na tabulku do zoo.
# Popisek bude využívat sloupců title (název zvířete), food (typ stravy), food_note (vysvětlující doplněk ke stravě) a description (jak zvíře poznáme).
# Napiš funkci popisek, která bude mít jeden parametr radek. Funkce spojí informace dohromady. Následně použijte metodu apply, abyste vytvořili nový sloupec s tímto popiskem.

# Fill null values
lexikon_zvirat = lexikon_zvirat.fillna('')

# print(lexikon_zvirat.head().to_string())
# print(lexikon_zvirat.iloc[320, :])

def popisek(radek):
    return radek.title + ' preferuje následující typ stravy: ' + radek.food + '. Konkrétně ocení když mu do misky přistanou ' + radek.food_note + '.'\
           '\nJak toto zvíře poznáme: ' + radek.description

lexikon_zvirat["popisek"] = lexikon_zvirat.apply(popisek, axis=1)

# Zvire na pozici 320
print(lexikon_zvirat.iloc[320, -1])
# Zvire na pozici 300
print(lexikon_zvirat.iloc[300, -1])
