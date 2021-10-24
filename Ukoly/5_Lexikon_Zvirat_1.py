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
# print(lexikon_zvirat.info())
lexikon_zvirat = lexikon_zvirat.dropna(how="all", axis="columns")
lexikon_zvirat = lexikon_zvirat.dropna(how="all", axis="rows")
lexikon_zvirat = lexikon_zvirat.set_index(["id"])
# print(lexikon_zvirat.tail().to_string())

####################################################################
# Lexikon zvirat 1
####################################################################
# Dataset obsahuje sloupec image_src, který má jako hodnoty odkazy na fotky jednotlivých zvířat.
# Například odkaz https://zoopraha.cz/images/lexikon-images/Drozd_oranIovohlav_.jpg vede na fotku drozda oranžovohlavého:
# Napiš funkci check_url, která bude mít jeden parametr radek. Funkce zkontroluje, jestli je odkaz v pořádku podle několika pravidel.
# K odkazu přistoupíš v těle funkce přes tečkovou notaci: radek.image_src. Zkontroluj následující:
# datový typ je řetězec: isinstance(radek.image_src, str)
# hodnota začíná řetězcem "https://zoopraha.cz/images/": radek.image_src.startswith("https://zoopraha.cz/images/") 3.hodnota končí buďto JPG nebo jpg.
# Zvol si jeden ze způsobů procházení tabulky, a na každý řádek zavolej funkci check_url. Pro každý řádek s neplatným odkazem vypiš název zvířete (title).

def check_url(radek):
    if isinstance(radek.image_src, str) & radek.image_src.startswith("https://zoopraha.cz/images/") & (radek.image_src.endswith("JPG") | radek.image_src.endswith("jpg")):
        result = "corect_url"
    else:
        result = radek.title
    return result

# Print rows with null values in image_src
# print(lexikon_zvirat[lexikon_zvirat["image_src"].isna()].to_string())
# Fill null values
lexikon_zvirat = lexikon_zvirat.fillna('')

# Check url using function check_url
lexikon_zvirat["url"] = lexikon_zvirat.apply(check_url, axis=1)
lexikon_zvirat_filtered = lexikon_zvirat[["title", "image_src", "url"]]
print(lexikon_zvirat_filtered.head(n=70).to_string())

