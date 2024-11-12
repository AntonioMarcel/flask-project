import os
import sys

# Ajusta o caminho do PYTHONPATH para o diretório raiz da aplicação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csv import reader

from app import app, db
from app.models import OrdenadorDespesas

with app.app_context():
  with open("scripts/ordenador_despesas.csv") as f:
        csv_reader = reader(f, delimiter=";")
        next(csv_reader)
        ordenadores = dict()

        for row in csv_reader:
          if row[0] and row[1]: # remove empty lines
            ordenadores[row[0]] = row[1]

        # print(ordenadores)

        for masp, nome in ordenadores.items():
          ordenador = OrdenadorDespesas(masp=masp,nome=nome)
          db.session.add(ordenador)
        
        db.session.commit()

# definir depois CLI para esse script

  # ordenadores = {}

  # for row in csv_reader:
  #   if first_line:
  #     first_line = False
  #     continue

  #   if row[0] and row[1]:
  #     ordenadores[row[0]] = row[1]
      

# from csv import reader
# from sqlite3 import connect

# insert_ordenador = "INSERT INTO ordenador_despesas (masp, nome) VALUES (?,?)"
# conn = connect("app.db")

# try:
#   with open("scripts/ordenador_despesas.csv") as f:
#     cur = conn.cursor()
#     first_line = True
#     csv_reader = reader(f, delimiter=";")
#     ordenadores = {}

#     for row in csv_reader:
#       if first_line:
#         first_line = False
#         continue

#       if row[0] and row[1]:
#         ordenadores[row[0]] = row[1]
      
#     for masp, nome in ordenadores.items():
#       cur.execute(insert_ordenador, [masp, nome])

#     conn.commit()

#     print(ordenadores) 
# except:
#   conn.rollback()
# finally:
#   conn.close()