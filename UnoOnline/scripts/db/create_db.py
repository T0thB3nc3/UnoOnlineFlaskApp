import sqlite3
import os

# A script helyének meghatározása
script_dir = os.path.dirname(os.path.abspath(__file__))

# Adatbázis fájl elérési útja a script mappájában
db_file = os.path.join(script_dir, "game_database.db")

# SQL script elérési útja a script mappájában
sql_file_path = os.path.join(script_dir, "dbscript.sql")

# Adatbázis fájl létrehozása vagy megnyitása
connection = sqlite3.connect(db_file)

# SQL script betöltése és végrehajtása
with open(sql_file_path, "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()

# SQL script futtatása
connection.cursor().executescript(sql_script)

# Adatbázis mentése és kapcsolat lezárása
connection.commit()
connection.close()

print(f"Az adatbázis létrejött: {db_file}")

