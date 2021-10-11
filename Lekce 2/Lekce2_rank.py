import datetime
import pandas
import requests
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/ioef.csv")
open("ioef.csv", 'wb').write(r.content)

ioef = pandas.read_csv("ioef.csv")
ioef["rank"] = ioef.groupby(["Index Year"])["Overall Score"].rank(ascending=False)
ioef = ioef.sort_values(["Name", "Index Year"])
ioef["rank_previous_year"] = ioef.groupby(["Name"])["rank"].shift()
ioef["Difference"] = ioef["rank"] - ioef["rank_previous_year"]
print(ioef.head())