import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split, GridSearchCV

r = requests.get(
    "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/auto.csv"
)
open("auto.csv", "wb").write(r.content)

####################################################################
# Zadání
####################################################################
# Pracuj se souborem auto.csv. Obsahuje informace o vyráběných modelech aut mezi lety 1970-1982.
# Načti data. Při volání metody read_csv nastav parametr na_values: na_values=["?"]

data = pd.read_csv("auto.csv", na_values=["?"])
print(data.head().to_string())
print(data.isna().sum())

# Po načtení dat se zbav řádek, které mají nějakou neznámou/prázdnou hodnotu (nápověda: dropna).
data = data.dropna()

# Podívej se, jak se měnila spotřeba aut v letech 1970-1982.
# Vytvoř graf, který ukáže průměrnou spotřebu v jednotlivých letech.
data_pivot = pd.pivot_table(data, index=["year"], columns=["origin"], values=["mpg"], aggfunc=np.mean)
print(data_pivot)
data_pivot.plot()
plt.show()

# Z dat odeber sloupec "name", který nebudeme pro predikci používat.
data = data.drop(columns=["name"])

# Rozděl data na vstupní a výstupní proměnnou, a následně na trénovací a testovací sadu v poměru 70:30.
X = data.drop(columns="origin")
y = data["origin"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
# print(X_train.shape, y_train.shape)
# print(X_test.shape, y_test.shape)

# Data normalizuj
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Použij klasifikační algoritmus rozhodovacího stromu, a vyber jeho parametry technikou GridSearchCV
model = DecisionTreeClassifier(random_state=0)
clf = GridSearchCV(model, param_grid={"max_depth": [5, 10, 20, 40], "min_samples_leaf": [1, 3, 5]}, scoring="f1_weighted")

# Jaké jsi dosáhl/a metriky f1_score?
clf.fit(X_train, y_train)
print(round(clf.best_score_, 2))
print(clf.best_estimator_)