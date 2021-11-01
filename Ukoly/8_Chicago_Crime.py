import pandas as pd
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt

####################################################################
# Zadání
####################################################################
# Tabulka crime v naší databázi obsahuje informace o kriminalitě v Chicagu.
# Dataset je poměrně velký, a tak si určitě vytáhneme vždy jen nějaký výběr, se kterým budeme dále pracovat.
# Pomocí SQL dotazu si připrav tabulku o krádeži motorových vozidel (sloupec PRIMARY_DESCRIPTION by měl mít hodnotu "MOTOR VEHICLE THEFT").
# Tabulku dále pomocí pandasu vyfiltruj tak, aby obsahovala jen informace o krádeži aut (hodnota "AUTOMOBILE" ve sloupci SECONDARY_DESCRIPTION).
# Ve kterém měsíci dochází nejčastěji ke krádeži auta?

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "hizova.k"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "dQ80vPm5eK!H!YcE"

#dialect+driver://username:password@host:port/database
engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

inspector = inspect(engine)
# print(inspector.get_table_names())
# print(inspector.get_columns('crime'))

df = pd.read_sql("SELECT * FROM crime WHERE \"PRIMARY_DESCRIPTION\" = 'MOTOR VEHICLE THEFT'", con=engine)
df_filtered = df[df["SECONDARY_DESCRIPTION"] == "AUTOMOBILE"].reset_index(drop=True)
df_filtered["MONTH"] = pd.to_datetime(df_filtered["DATE_OF_OCCURRENCE"]).dt.month
# print(df_filtered.head(n=50).to_string())
df_grouped = df_filtered.groupby(["MONTH"]).size().to_frame("COUNT")
df_grouped = df_grouped.sort_values(["COUNT"], ascending=False).reset_index(drop=False)
print(df_grouped)

print("Nejčastěji dochází v Chicagu ke krádeži aut v září.")