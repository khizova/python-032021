import pandas as pd
import math

sportoviste = pd.read_json("sportoviste.json")
sportoviste = sportoviste.dropna(how="all", axis="columns")
sportoviste = sportoviste.set_index("OBJECTID")
print(sportoviste.head().to_string())

sportoviste = sportoviste.rename(columns={"POINT_Y": "zemepisna_sirka", "POINT_X": "zemepisna_delka"})

poloha_nadrazi_opava = [49.9345092, 17.9085369]

def vzdalenost_od_bodu(radek, bod):
    # Vypocet vzdalenosti mezi dvema body (Eukleidovska vzdalenost)
    vzdalenost = math.sqrt((bod[0] - radek.zemepisna_sirka) ** 2 + (bod[1] - radek.zemepisna_delka) ** 2)
    # Prevod na vzdalenost v kilometrech a zaokrouhleni
    vzdalenost_km = vzdalenost * (2.0 * 6371 * math.pi / 360.0)
    vzdalenost_km = round(vzdalenost_km, 2)
    return vzdalenost_km

sportoviste["vzdalenost_od_nadrazi_v_km"] = sportoviste.apply(vzdalenost_od_bodu, axis=1, args=(poloha_nadrazi_opava,))
print(sportoviste.sort_values("vzdalenost_od_nadrazi_v_km")[["prostor", "sportoviste_nazev", "vzdalenost_od_nadrazi_v_km"]].head().to_string())

