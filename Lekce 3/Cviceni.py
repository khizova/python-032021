import pandas as pd

adopce = pd.read_csv("adopce-zvirat.csv", sep=";")
adopce = adopce.dropna(how="all", axis="columns")
adopce = adopce.dropna(how="all", axis="rows")

# adopce_filtered = pd.DataFrame()
#
# for index, zvire in adopce.iterrows():
#     if "blue" in zvire["nazev_en"].lower():
#         if zvire["cena"] <= 2500:
#             if zvire["k_prohlidce"]:
#                 adopce_filtered = adopce_filtered.append(zvire, ignore_index=True)
# print(adopce_filtered.to_string())

# adopece_filtered_dotaz = adopce[(adopce.k_prohlidce == 1.0) & (adopce.cena <= 2500) & (adopce.nazev_en.str.lower().str.contains("blue"))]
# print(adopece_filtered_dotaz.to_string())

# adopece_filtered_dotaz = adopce[(adopce["k_prohlidce"] == 1.0) & (adopce["cena"] <= 2500) & (adopce["nazev_en"].str.contains("blue", case=False))]
# print(adopece_filtered_dotaz.to_string())

adopece_filtered_dotaz = adopce[(adopce["k_prohlidce"] == 1.0) & (adopce["cena"] <= 2500) & (adopce["nazev_en"].str.lower().str.contains("blue"))]
print(adopece_filtered_dotaz.to_string())