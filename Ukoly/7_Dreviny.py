import pandas as pd
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt
import numpy as np

####################################################################
# Připojení k databázi
####################################################################
# Pomocí SQL dotazu do databáze si připrav dvě pandas tabulky:
# tabulka smrk bude obsahovat řádky, které mají v sloupci dd_txt hodnotu "Smrk, jedle, douglaska"
# tabulka nahodila_tezba bude obsahovat řádky, které mají v sloupci druhtez_txt hodnotu "Nahodilá těžba dřeva"

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
# print(inspector.get_columns('dreviny'))

####################################################################
# Smrk
####################################################################
# Vytvoř graf, který ukáže vývoj objemu těžby pro tabulku smrk. Pozor, řádky nemusí být seřazené podle roku.
smrk = pd.read_sql("SELECT * FROM dreviny WHERE dd_txt = 'Smrk, jedle, douglaska'", con=engine)
smrk = smrk.sort_values(["rok"])
smrk["hodnota"] = smrk["hodnota"]/1_000_000
# print(smrk.to_string())
smrk.plot.bar(x="rok", y="hodnota", legend=None)
plt.title("Vývoj objemu těžby smrků, jedel a douglasek v rocích 2000-2020", fontsize=12, pad=15)
plt.ylabel("Těžba dřeva (mil. $\mathregular{m^{3}}$)")
plt.show()

####################################################################
# Nahodilá těžba
####################################################################
# Vytvoř graf (nebo několik grafů), který ukáže vývoj objemu těžby v čase pro všechny typy nahodilé těžby.
nahodila_tezba = pd.read_sql("SELECT * FROM dreviny WHERE druhtez_txt = 'Nahodilá těžba dřeva'", con=engine)
nahodila_tezba = nahodila_tezba.dropna(subset=["prictez_txt"])
# nahodila_tezba["prictez_txt"] = np.where(nahodila_tezba["prictez_txt"].isna(), "Neznáma příčina", nahodila_tezba["prictez_txt"])
nahodila_tezba["hodnota"] = nahodila_tezba["hodnota"]/1_000_000
nahodila_tezba_pivot = pd.pivot_table(nahodila_tezba, index="rok", columns="prictez_txt", values="hodnota", aggfunc=np.sum).plot.bar()
plt.xlabel("")
plt.ylabel("Těžba dřeva (mil. $\mathregular{m^{3}}$)")
plt.legend(title="Příčiny nahodilé těžby")
plt.title("Vývoj objemu těžby v čase pro různé typy nahodilé těžby dřeva", fontsize=12, pad=15)
plt.show()

####################################################################
# Dobrovolný doplněk
####################################################################
# Čím je způsobený prudký nárůst těžby jehličnatých stromů cca od roku 2015, který je viditelný v grafu z bodu (2.)?
print("V roce 2015 zasáhla Českou republiku největší kůrovcová kalamita od dob Marie Terezie. Začala na severní Moravě, kde kůrovec napadl suchem oslabené smrky.")
# Kolem roku 2007 vidíme v obou grafech krátkodobý nárůst těžby. Čím byl způsobený (můžeš zkusit dohledat konkrétní událost)?
print("Výrazný co do těžby byl i rok 2007, kdy se vytěžilo 18,5 milionů m3 dřeva, tehdy ale za mohutné kácení mohl orkán Kyrill, který za sebou nechal spoušť po celé Evropě."
      "V roce 2007 proto 85 % těžby představovala těžba živelní, která měla za úkol odklidit následky této přírodní katastrofy."
      "Největší škody orkán napáchal v okrese Klatovy, kde po osmihodinovém řádění zničil téměř 3 miliony m3 dřeva.")