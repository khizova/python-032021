import datetime
import pandas
import requests
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/baroko_half_marathon.csv")
open("baroko_half_marathon.csv", 'wb').write(r.content)

baroko_half_marathon = pandas.read_csv("baroko_half_marathon.csv")
baroko_half_marathon = baroko_half_marathon.sort_values(["Jméno závodníka", "Ročník", "Rok závodu"])
baroko_half_marathon["FINISH"] = pandas.to_datetime(baroko_half_marathon["FINISH"])
baroko_half_marathon = baroko_half_marathon[["Jméno závodníka", "Ročník", "Rok závodu", "FINISH"]]
baroko_half_marathon["finish_previous_year"] = baroko_half_marathon.groupby(["Jméno závodníka", "Ročník"])["FINISH"].shift()
print(baroko_half_marathon.head())

baroko_half_marathon_new = baroko_half_marathon.dropna(subset=["finish_previous_year"]).reset_index(drop=True)
baroko_half_marathon_new["rozdil"] = baroko_half_marathon_new["FINISH"] - baroko_half_marathon_new["finish_previous_year"]
baroko_half_marathon_new["diff_text"] = numpy.where(baroko_half_marathon_new["rozdil"] > pandas.Timedelta("P0D"), "zhorseni", "zlepseni")
print(baroko_half_marathon_new["diff_text"].value_counts())
print(baroko_half_marathon_new.groupby)


desired_width = 1000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',100)

