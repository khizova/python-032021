import datetime
import pandas
import requests
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices.csv")
open("invoices.csv", 'wb').write(r.content)

invoices = pandas.read_csv("invoices.csv")
invoices["invoice_date_coverted"] = pandas.to_datetime(invoices["invoice_date"], format="%d. %m. %Y")
invoices["due_date"] = invoices["invoice_date_coverted"] + pandas.Timedelta("P60D")
today_date = datetime.datetime(2021, 9, 1)
invoices["status"] = numpy.where(invoices["due_date"] < today_date, "overdue", "pred splatnosti")
print(invoices.groupby("status")["amount"].sum())

