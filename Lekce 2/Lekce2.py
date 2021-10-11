import requests
import pandas

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/data_with_ids.csv")
open("../Lekce 1/data_with_ids.csv", 'wb').write(r.content)

data_with_ids = pandas.read_csv("../Lekce 1/data_with_ids.csv")
print(data_with_ids.shape[0])

print(data_with_ids["bank_id"].nunique())
data_with_ids_unique = data_with_ids.drop_duplicates(ignore_index=True)
print(data_with_ids_unique.head())
print(data_with_ids_unique.shape)