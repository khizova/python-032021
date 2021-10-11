import requests
import pandas as pd
import numpy as np

#r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/titanic.csv")
#open("titanic.csv", 'wb').write(r.content)

# V souboru titanic.csv najdeš informace o cestujících na zaoceánském parníku Titanic.
# Vytvoř kontingenční tabulku, která porovná závislost mezi pohlavím cestujícího (soupec Sex), třídou (sloupec Pclass), ve které cestoval, a tím, jesti přežil potopení Titanicu (sloupec Survived).
# Pro data můžeš použít agregaci len, numpy.sum, která ti spočte absolutní počet přeživších pro danou kombinaci, nebo numpy.mean, která udá relativní počet přeživších pro danou kombinaci.

titanic = pd.read_csv("titanic.csv")
print(titanic.columns)
print(titanic.head())

# Prehledova tabulka pomoci agregace
titanic_aggregated_sum = titanic.groupby(["Sex", "Pclass"])["Survived"].sum()
titanic_aggregated_sum = pd.DataFrame(titanic_aggregated_sum)
print(titanic_aggregated_sum)

titanic_aggregated_mean = titanic.groupby(["Sex", "Pclass"])["Survived"].mean()
titanic_aggregated_mean = pd.DataFrame(titanic_aggregated_mean)
print(titanic_aggregated_mean)

# Kontingencni tabulka pomoci funkci pivot_table
titanic_pivot_absolute = pd.pivot_table(titanic, index="Sex", columns="Pclass", values="Survived", aggfunc=np.sum, margins=True)
print("Absolutní počet přeživších pro jednotlivé kombinace pohlavní a třídy: \n", titanic_pivot_absolute)

# Rozšířené zadání
# Z dat vyfiltruj pouze cestující, kteří cestovali v první třídě. Dále použij metodu cut na rozdělení cestujících do věkových skupin (zkus vytvořit např. 4 skupiny, můžeš definovat hranice skupin tak, aby vznikly skupiny děti, teenageři, dospělí a senioři).
# Urči relativní počet přeživších pro jednotlivé kombinace pohlavní a věkové skupiny.

titanic_first_class = titanic[titanic.Pclass == 1]
titanic_first_class = pd.DataFrame(titanic_first_class)
print("Min age: ", titanic_first_class["Age"].min())
print("Max age: ", titanic_first_class["Age"].max())
titanic_first_class["age_group"] = pd.cut(titanic_first_class["Age"], bins=[0, 10, 18, 65, 100])
titanic_pivot_age_groups = pd.pivot_table(titanic_first_class, index="Sex", columns="age_group", values="Survived", aggfunc=np.sum, margins=True)
titanic_pivot_age_groups_percentage = titanic_pivot_age_groups.div(titanic_pivot_age_groups.iloc[:,-1], axis=0)
print("Absolutní počet přeživších pro jednotlivé kombinace pohlaví a věkové skupiny v první třídě: \n", titanic_pivot_age_groups)
print("Relativní počet přeživších pro jednotlivé kombinace pohlaví a věkové skupiny v první třídě: \n", titanic_pivot_age_groups_percentage)

