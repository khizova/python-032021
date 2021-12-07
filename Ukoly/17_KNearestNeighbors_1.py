import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, precision_score, f1_score, accuracy_score, recall_score
import matplotlib.pyplot as plt

# 1. Definice problemu
# Je voda pitná nebo ne (na základě jejího chemického rozboru)

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/water-potability.csv")
open("water-potability.csv", 'wb').write(r.content)

# 2. Data
data = pd.read_csv("water-potability.csv")
print(data.head().to_string())
# print(data.isna().sum())
data = data.dropna()
print(data.shape)

# Rozdeleni cilovych hodnot
print(data["Potability"].value_counts(normalize=True))

X = data.drop(columns=["Potability"])
y = data["Potability"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# print(X_train.shape, y_train.shape)
# print(X_test.shape, y_test.shape)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. + 4
clf = KNeighborsClassifier()
clf.fit(X_train, y_train)
print(clf)

# 5. Vyhodnoceni modelu
y_pred = clf.predict(X_test)

print(confusion_matrix(y_true=y_test, y_pred=y_pred))

# ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
#                                       display_labels=clf.classes_,
#                                       cmap=plt.cm.Blues)
# plt.show()

ks = [1, 3, 5, 7, 9, ]
for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(k, precision_score(y_test, y_pred))

# Zaverecna predikce
clf = KNeighborsClassifier(n_neighbors=9)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(precision_score(y_test, y_pred))

# Liší se tvůj zvolený parametr od parametru, který jsme jako závěrečný zvolili v lekci?
print("Parametr se liší od parametru, který jsme jako závěrečný zvolili v lekci.")

# Jak vypadá matice chyb (confusion matrix)?
# ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
#                                       display_labels=clf.classes_,
#                                       cmap=plt.cm.Blues)
# plt.show()

# Dovedeš z matice odvodit výpočet, který nám dá stejnou hodnotu, jako při použití metody precision()?
print(67 / (67 + 43))
print(precision_score(y_test, y_pred))

####################################################################
# Dobrovolný doplněk
####################################################################
# Vytvoř graf, který bude pro několik parametrů n_neighbors obsahovat všechny čtyři výsledné metriky, které jsme si v kurzu ukázali: accuracy, precision, recall, f1_score.

ks = [1, 3, 5, 7, 9]
f1_scores = []
accuracy_scores = []
recall_scores = []
precision_scores = []
for k in ks:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_scores.append(f1_score(y_test, y_pred))
    accuracy_scores.append(accuracy_score(y_test, y_pred))
    recall_scores.append(recall_score(y_test, y_pred))
    precision_scores.append(precision_score(y_test, y_pred))

plt.plot(ks, f1_scores, label="f1_scores")
plt.plot(ks, accuracy_scores, label="accuracy_scores")
plt.plot(ks, recall_scores, label="recall_scores")
plt.plot(ks, precision_scores, label="precision_scores")
plt.legend()
plt.show()
