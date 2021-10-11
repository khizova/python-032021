import pandas
import requests
r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/covid_data.csv")
open("../Lekce 1/covid_data.csv", 'wb').write(r.content)

covid_data = pandas.read_csv("../Lekce 1/covid_data.csv")
covid_data = covid_data.drop_duplicates(subset=["date"], keep="last")
print(covid_data.head())