import requests
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

r = requests.get(
    "https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/soybean-2-rot.csv"
)
open("soybean-2-rot.csv", "wb").write(r.content)

data = pd.read_csv("soybean-2-rot.csv")

X = data.drop(columns=["class"])
input_features = X.columns
# print(input_features)

y = data["class"]

oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0
)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"))

# Která vstupní proměnná má největší "důležitost"?
importances = clf.feature_importances_
clf_importances = pd.Series(importances, index=oh_encoder.get_feature_names(input_features=input_features))
clf_importances.plot.bar()
# plt.show()

print("Největší důležitost má vstupní proměnná plant-stand.")

# Stačí nám tato proměnná pro úspěšnou klasifikaci?
# Jaký je rozdíl mezi hodnotou f1_score při použití všech proměnných a jen této jedné "nejdůležitější" proměnné?
X = data[["plant-stand"]]
y = data["class"]

oh_encoder = OneHotEncoder()
X = oh_encoder.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0
)

clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(f1_score(y_test, y_pred, average="weighted"))

print("Při použití jen této jedné nejdůležitější proměnné klesne hodnota f1_score z 0.928 na 0.753.")

