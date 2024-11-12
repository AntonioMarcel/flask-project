import os
import sys

# Ajusta o caminho do PYTHONPATH para o diretório raiz da aplicação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from csv import reader

from app import app, db
from app.models import DadosEmpenhos, OrdenadorDespesas, User

with app.app_context():
    with open("scripts/dados_empenhos.csv", encoding="latin-1") as f:
        csv_reader = reader(f, delimiter=";")
        next(csv_reader)
        dados_empenhos = []

        for row in csv_reader:
            if any(row):
                dados_empenhos.append(
                    {
                        "uo": row[1],
                        "ue": row[2],
                        "ano": row[3],
                        "empenho": row[4],
                        "projeto_atividade": row[5],
                        "gmi_fp": row[6],
                        "elemento_item": row[7],
                        "razao_social_credor": row[8],
                        "cnpj_cpf_credor": row[9],
                    }
                )

        for row in dados_empenhos:
            data_emp = DadosEmpenhos(
                uo=row["uo"],
                ue=row["ue"],
                ano=row["ano"],
                empenho=row["empenho"],
                projeto_atividade=row["projeto_atividade"],
                gmi_fp=row["gmi_fp"],
                elemento_item=row["elemento_item"],
                razao_social_credor=row["razao_social_credor"],
                cnpj_cpf_credor = row["cnpj_cpf_credor"]
            )
            db.session.add(data_emp)


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

          user = User(username="xarope", email="xarope@gmail.com")
          user.set_password("xarope123")
          db.session.add(user)

          db.session.commit()