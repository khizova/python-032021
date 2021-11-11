import pandas as pd
from scipy.stats.mstats import gmean

####################################################################
# Zadání
####################################################################
# V souboru crypto_prices.csv najdeš ceny různých kryptoměn v průběhu času.
# Datum je ve sloupci Date a název kryptoměny ti prozradí sloupec Name, alternativně můžeš využít sloupec Symbol.
# Z datového souboru si vyber jednu kryptoměnu a urči průměrné denní tempo růstu měny za sledované období.
# Můžeš využít funkci geometric_mean z modulu statistics.
# Vyber si sloupec se změnou ceny, kterou máš vypočítanou z předchozího cvičení (případně si jej dopočti), přičti k němu 1 (nemusíš dělit stem jako v lekci, hodnoty jsou jako desetinná čísla, nikoli jako procenta) a převeď jej na seznam pomocí metody .tolist().
# Následně vypočti geometrický průměr z těchto hodnot.

df = pd.read_csv("crypto_prices.csv")
df = df[["Date", "Symbol", "Close"]]
df["pct_change"] = df.groupby(["Symbol"])["Close"].pct_change()
# print(df.head(n=100).to_string())

xmr = df[df["Symbol"] == "XMR"]["pct_change"].dropna()
xmr_list = (xmr + 1).to_list()
# print(xmr_list)

xmr_mean = gmean(xmr_list) - 1
print(f"Průměrný mezidenní růst ceny XMR je", xmr_mean)






