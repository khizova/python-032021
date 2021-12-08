import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, f1_score
import matplotlib.pyplot as plt

r = requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/kosatce.csv")
open("kosatce.csv", "wb").write(r.content)

# Data prepation
data = pd.read_csv("kosatce.csv")
print(data.head().to_string())
print(data.isna().sum())

# Dataset split
print(data["target"].value_counts(normalize=True))
X = data.drop(columns=["target"])
y = data["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# print(X_train.shape, y_train.shape)
# print(X_test.shape, y_test.shape)

# Algorithm choice and model training
clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

# Model evaluation
y_pred = clf.predict(X_test)

ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test,
                                      display_labels=clf.classes_,
                                      cmap=plt.cm.Blues)
# plt.show()

print(f1_score(y_test, y_pred))
print("Použitím algoritmu KNeighborsClassifier je možné předpovědět typ kosatce na základě těchto dat tak, aby metrika f1_score dosáhla alespoň 85%.")

