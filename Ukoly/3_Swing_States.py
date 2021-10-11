import requests
import pandas as pd
import numpy as np

# with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/1976-2020-president.csv") as r:
#   open("1976-2020-president.csv", 'w', encoding="utf-8").write(r.text)

# V případě amerických prezidentských voleb obecně platí, že ve většině států dlouhodobě vyhrávají kandidáti jedné strany.
# Například v Kalifornii vyhrává kandidát Demokratické strany or roku 1992, v Texasu kandidát Republikánské strany od roku 1980, v Kansasu do konce od roku 1968 atd.
# Státy, kde se vítězné strany střídají, jsou označovány jako "swing states" ("kolísavé státy").
# Tvým úkolem je vybrat státy, které lze označit jako swing states.
#
# V souboru 1976-2020-president.csv najdeš historické výsledky amerických prezidentských voleb.
# Každý řádek souboru obsahuje počet hlasů pro kandidáta dané strany v daném roce.
#
# V souboru jsou důležité následující sloupce:
#
# Year - rok voleb,
# State - stát,
# party_simplified - zjednodušené označení politické strany,
# candidatevotes - počet hlasů pro vybraného kandidáta,
# totalvotes - celkový počet odevzdaných hlasů.

# Proveď níže uvedené úkoly.
#
# Úkol ber spíše jako návod k řešení, není nutné je přesně dodržovat. Důležité je pouze dospět k požadovaném závěru nebo nějakému obdobnému a možná ještě zajímavějšímu závěru :-)
#
# Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()). Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby().
# Pro další analýzu jsou důležití pouze vítězové. Ponech si v tabulce pouze řádky, které obsahují vítěze voleb v jednotlivých letech v jednotlivých státech.
# Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany ve dvou po sobě jdoucích letech.
# Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana. Můžeš k tomu použít např. funkce numpy.where a vložit hodnotu 0 nebo 1 podle toho, jestli došlo ke změně vítězné strany.
# Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.

elections = pd.read_csv("1976-2020-president.csv")
print(elections.head().to_string())

# Check and remove null values
print(elections["candidate"].isnull().sum())
elections = elections.dropna(subset=["candidate"]).reset_index()
print(elections["candidate"].isnull().sum())

elections["rank"] = elections.groupby(["year", "state"])["candidatevotes"].rank(method="min", ascending=False)
print(elections[(elections["state"] == "ALABAMA") & ((elections["year"] == 1976) | (elections["year"] == 1980))].to_string())
elections = elections[elections["rank"] == 1]
elections = elections.sort_values(["state", "year"])
elections["party_previous_year"] = elections.groupby(["state"])["party_detailed"].shift()
elections["party_change"] = np.where((elections["party_detailed"] != elections["party_previous_year"]) & (elections["party_previous_year"].notna()), 1, 0)
# print(elections.to_string())

elections_swing_states = pd.DataFrame(elections.groupby(["state"])["party_change"].sum())
elections_swing_states = elections_swing_states.sort_values("party_change", ascending=False).reset_index()
elections_swing_states = elections_swing_states.rename(columns={"party_change" : "number_of_party_changes"})
print("Přehled swing states amerických prezidenstkých voleb: \n", elections_swing_states[elections_swing_states["number_of_party_changes"] > 0])

# Dobrovolný doplněk
# U amerických voleb je zajímavý i tzv. margin, tedy rozdíl mezi prvním a druhým kandidátem.
#
# Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí. Nezapomeň, že je k tomu potřeba kompletní dataset, tj. je potřeba tabulku znovu načíst, protože v předchozí části jsme odebrali některé řádky.
# Můžeš přidat i sloupec s relativním marginem, tj. rozdílem vyděleným počtem hlasů.
# Seřaď tabulku podle velikosti margin (absolutním i relativním) a zjisti, kde byl výsledek voleb nejtěsnější.

#############################################################################################################
# Nejmensi rozdil v hlasovani na urovni statu
#############################################################################################################
elections_margin = pd.read_csv("1976-2020-president.csv")
elections_margin = elections_margin.dropna(subset=["candidate"]).reset_index(drop=True)
elections_margin["rank"] = elections_margin.groupby(["year", "state"])["candidatevotes"].rank(method="min", ascending=False)
elections_margin = elections_margin[elections_margin["rank"] < 3]
elections_margin["second_rank_votes"] = elections_margin.groupby(["state", "year"])["candidatevotes"].shift(-1)
elections_margin["absolute_margin"] = elections_margin["candidatevotes"] - elections_margin["second_rank_votes"]
elections_margin["relative_margin"] = elections_margin["absolute_margin"] / elections_margin["totalvotes"]
# print(elections_margin[(elections_margin["state"] == "ALABAMA") & ((elections_margin["year"] == 1976) | (elections_margin["year"] == 1980) | (elections_margin["year"] == 1984) | (elections_margin["year"] == 1984))].to_string())

elections_margin = elections_margin[elections_margin["rank"] == 1]
elections_margin = elections_margin.sort_values("absolute_margin", ascending=True).reset_index(drop=True)
candidate_converted = elections_margin["candidate"].str.split(pat=",", n=1, expand=True)
elections_margin["candidate_name_converted"] = candidate_converted[1] + " " + candidate_converted[0]
elections_margin["state"] = elections_margin["state"].str.title()
elections_margin["candidate_name_converted"] = elections_margin["candidate_name_converted"].str.title()
print(elections_margin.head().to_string())

#############################################################################################################
# Nejmensi rozdil celkove mezi kandidaty v jednotlivych volbach
#############################################################################################################
elections_margin_grouped = pd.read_csv("1976-2020-president.csv")
elections_margin_grouped = elections_margin_grouped.dropna(subset=["candidate"]).reset_index(drop=True)
elections_margin_grouped = elections_margin_grouped.groupby(["year", "candidate"])["candidatevotes"].sum().reset_index()
elections_margin_grouped["rank"] = elections_margin_grouped.groupby(["year"])["candidatevotes"].rank(ascending=False)
elections_margin_grouped = elections_margin_grouped.sort_values(["year", "candidatevotes"], ascending=False)
elections_margin_grouped = elections_margin_grouped[elections_margin_grouped["rank"] < 3]
elections_margin_grouped["second_rank_votes"] = elections_margin_grouped.groupby(["year"])["candidatevotes"].shift(-1)
elections_margin_grouped = elections_margin_grouped[elections_margin_grouped["rank"] == 1]
elections_margin_grouped["margin"] = elections_margin_grouped["candidatevotes"] - elections_margin_grouped["second_rank_votes"]
elections_margin_grouped = elections_margin_grouped.sort_values(["margin"], ascending=True).reset_index(drop=True)
candida_name_converted = elections_margin_grouped["candidate"].str.split(pat=",", n=1, expand=True)
elections_margin_grouped["candidate_name_converted"] = candida_name_converted[1] + " " + candida_name_converted[0]
elections_margin_grouped["candidate_name_converted"] = elections_margin_grouped["candidate_name_converted"].str.title()
print(elections_margin_grouped.to_string())

print("Nejtěsnější výsledek amerických prezidenstkých voleb byl v roce ", elections_margin_grouped["year"][0],
      ", kdy ", elections_margin_grouped["candidate_name_converted"][0], " vyhrál s rozdílem ", elections_margin_grouped["margin"][0], " hlasů. "
      "Nejtěsnější výsledek na úrovni jednotlivých států jsme zaznamenali v roce ", elections_margin["year"][0], " ve státu ", elections_margin["state"][0],
      ", kde ", elections_margin["candidate_name_converted"][0], " vyhrál s rozdílem ", elections_margin["absolute_margin"][0], " hlasů.",sep="")

