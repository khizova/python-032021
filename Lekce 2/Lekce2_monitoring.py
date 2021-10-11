import datetime
import pandas
import requests
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/signal_monitoring.csv")
open("signal_monitoring.csv", 'wb').write(r.content)

signal_monitoring = pandas.read_csv("signal_monitoring.csv")
signal_monitoring["event_date_time"] = pandas.to_datetime(signal_monitoring["event_date_time"])
signal_monitoring["event_date_time_2"] = signal_monitoring["event_date_time"].shift(-1)
signal_monitoring["event_length"] = signal_monitoring["event_date_time_2"] - signal_monitoring["event_date_time"]
signal_monitoring = signal_monitoring[signal_monitoring["event_type"] == "signal lost"]
print(signal_monitoring.head())