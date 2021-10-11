import datetime
import pandas
import requests
import numpy

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices_2.csv")
open("invoices_2.csv", 'wb').write(r.content)

invoices_2 = pandas.read_csv("invoices_2.csv")
invoices_2["invoice_date"] = pandas.to_datetime(invoices_2["invoice_date"], format="%d. %m. %Y")
invoices_2["payment_date"] = pandas.to_datetime(invoices_2["payment_date"], format="%d. %m. %Y")
print(invoices_2.head())

invoices_2_paid = invoices_2.dropna().reset_index(drop=True)
invoices_2_paid["paid_in"] = invoices_2["payment_date"] - invoices_2["invoice_date"]
print(invoices_2_paid.head())

average_payment_data = invoices_2_paid.groupby(["customer"])["paid_in"].mean()
average_payment_data = pandas.DataFrame(average_payment_data)
print(average_payment_data)

invoices_2_not_paid = invoices_2[invoices_2["payment_date"].isna()]
invoices_2_not_paid = pandas.merge(invoices_2_not_paid, average_payment_data, on=["customer"])
invoices_2_not_paid["expected_payment_date"] = invoices_2_not_paid["invoice_date"] + invoices_2_not_paid["paid_in"]
invoices_2_not_paid["expected_payment_date"] = invoices_2_not_paid["expected_payment_date"].dt.date
print(invoices_2_not_paid.head())