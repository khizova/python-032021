import requests
import pandas as pd
import statistics

# r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/crypto_prices.csv")
# open("crypto_prices.csv", "wb").write(r.content)

####################################################################
# Zadání
####################################################################
# V souboru crypto_prices.csv najdeš ceny různých kryptoměn v průběhu času.
# Datum je ve sloupci Date a název kryptoměny ti prozradí sloupec Name, alternativně můžeš využít sloupec Symbol.

# 1. Použij zavírací cenu kryptoměny (sloupec Close) a vypočti procentuální změnu jednotlivých kryptoměn.
# Pozor na to, ať se ti nepočítají ceny mezi jednotlivými měnami.
# Ošetřit to můžeš pomocí metody groupby(), jako jsme to dělali např. u metody shift().
df = pd.read_csv("crypto_prices.csv")
df = df[["Date", "Symbol", "Close"]]
df["pct_change"] = df.groupby(["Symbol"])["Close"].pct_change()
# print(df.head(n=100).to_string())

# 2. Vytvoř korelační matici změn cen jednotlivých kryptoměn a zobraz je jako tabulku.
df_pivot = pd.pivot(df, index="Date", columns="Symbol", values="pct_change")
# print(df_pivot.to_string())
# df_pivot_new = df_pivot.dropna(axis=0, how="any")
corr = df_pivot.corr()
print(corr.to_string())

# 3. V tabulce vyber dvojici kryptoměn s vysokou hodnotou koeficientu korelace a jinou dvojici s koeficientem korelace blízko 0.
# Změny cen pro dvojice měn, které jsou nejvíce a nejméně korelované, si zobraz jako bodový graf.
import seaborn as sns
import matplotlib.pyplot as plt

df_pivot_df = pd.DataFrame(df_pivot).reset_index()
wbtc = df_pivot_df[["Date", "WBTC"]]
# print(wbtc.head().to_string())

btc = df_pivot_df[["Date", "BTC"]]
# print(btc.head().to_string())

# Linearní závislost
wbtc_btc_joined = pd.merge(wbtc, btc, on="Date")
# print(wbtc_btc_joined.head().to_string())
sns.jointplot("WBTC", "BTC", wbtc_btc_joined, kind="scatter")
# plt.show()

# Linearní nezávislost
doge = df_pivot_df[["Date", "DOGE"]]
uni = df_pivot_df[["Date", "UNI"]]
doge_uni_joined = pd.merge(doge, uni, on="Date")
sns.jointplot("DOGE", "UNI", doge_uni_joined, kind="scatter", color="seagreen")
# plt.show()

# Linearní nezávislost
usdt = df_pivot_df[["Date", "USDT"]]
usdt_uni_joined = pd.merge(usdt, uni, on="Date")
sns.jointplot("USDT", "UNI", usdt_uni_joined, kind="scatter", color="seagreen")
# plt.show()

####################################################################
# Dobrovolný doplněk
####################################################################
# Spearmanova korelace
corr_spearman = df_pivot.corr(method="spearman")
print(corr_spearman.to_string())

# Select one month from frame
df_pivot_month = pd.DataFrame(df_pivot).reset_index()
df_pivot_month = df_pivot_month.iloc[2955:2985, :]
print(df_pivot_month.to_string())

# Correlation for June 2021
corr_month = df_pivot_month.corr()
print(corr_month.to_string())

# Show sorted correlation pairs
print(corr_month.unstack().sort_values().drop_duplicates())

# From original data select only rows for June 2021
crypto_close_price = df
crypto_close_price["Date"] = pd.to_datetime(crypto_close_price["Date"])
crypto_close_price["Date"] = pd.to_datetime(crypto_close_price["Date"].dt.date)
mask = (crypto_close_price["Date"] >= "2021-06-01") & (crypto_close_price["Date"] <= "2021-06-30")
# print(crypto_close_price.head(n=400).to_string())
crypto_close_price_june = crypto_close_price.loc[mask].reset_index(drop=True)
# print(crypto_close_price_june)

# Create tables for most and least correlating pairs - period June 2021
cro_june = crypto_close_price_june[crypto_close_price_june["Symbol"] == "CRO"]
usdc_june = crypto_close_price_june[crypto_close_price_june["Symbol"] == "USDC"]
wbtc_june = crypto_close_price_june[crypto_close_price_june["Symbol"] == "WBTC"]
btc_june = crypto_close_price_june[crypto_close_price_june["Symbol"] == "BTC"]

import matplotlib.gridspec as gridspec

# Least correlating pair
fig1 = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(2, 1)
ax = fig1.add_subplot(gs[0, 0])
ax.plot(cro_june["Date"], cro_june["Close"])
ax = fig1.add_subplot(gs[1, 0])
ax.plot(usdc_june["Date"], usdc_june["Close"])

# Most correlating pair
fig2 = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(2, 1)
ax = fig2.add_subplot(gs[0, 0])
ax.plot(wbtc_june["Date"], wbtc_june["Close"])
ax = fig2.add_subplot(gs[1, 0])
ax.plot(btc_june["Date"], btc_june["Close"])

plt.show()

print("Lineární závislot/nezávislost je možné vyčíst i z grafu vývoje zavírací ceny za kratší období.")

