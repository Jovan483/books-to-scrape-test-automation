import json
import mysql.connector
with open("proizvodi_i_cena.json","r", encoding="utf-8") as fajl:
    podaci_iz_jsona=json.load(fajl)
konekcija=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="knjizara",
    ssl_disabled=True #prevazilazim windows gresku
)
kursor=konekcija.cursor()
upit="INSERT INTO  naslov(naslov_knjige,cena_knjige)  VALUES(%s,%s)"

podaci_za_bazu=[(knjiga["title: "],knjiga["cena: "]) for knjiga in podaci_iz_jsona]
kursor.executemany(upit,podaci_za_bazu)
konekcija.commit()
kursor.close()
konekcija.close()

    
