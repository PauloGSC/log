# Copyright © 2021 Paulo Gabriel Sena Comasetto <paulogscomasetto@gmail.com>


import argparse
from copy import deepcopy
import re

import psycopg2 as psql
from terminaltables import SingleTable as Table


TABELA = "log" # tabela única do banco


# obtendo argumentos da linha de comando

psr = argparse.ArgumentParser(
	description="Programa para execução de log REDO."
)

psr.add_argument("arquivo") # caminho do arquivo, obrigatório
psr.add_argument("--banco", default="log") # opcional
psr.add_argument("--usuario", default="postgres") # opcional
psr.add_argument("--senha", default="postgres") # opcional

args = psr.parse_args()

# abrindo arquivo de log e extraindo o seu conteúdo

with open(args.arquivo) as arq:
	linhas = arq.read().splitlines()

# conectando-se ao banco

try:
	con = psql.connect(
		dbname=args.banco, user=args.usuario, password=args.senha
	)
except:
	print(f"Não foi possível conectar-se ao banco {args.banco}.")
	print("Abortando...")
	exit(1)

con.autocommit = True # habilita transações implícitas
cur = con.cursor()

# descobrindo colunas da tabela, conforme cabeçalho
# também coleta as chaves primárias (id)

cols = set()
ids = set()
for linha in linhas:
	linha2 = linha.replace(" ", "")

	if not linha2: # linha em branco, fim do cabeçalho
		break

	vga = linha2.find(",")

	col = linha2[:vga]
	cols.add(col)

	id_ = int(linha2[vga+1:linha2.find("=")])
	ids.add(id_)

cols = list(sorted(cols))
cols.insert(0, "id")
sql = [f"{col} INT" for col in cols]
sql += [f"PRIMARY KEY (id)"]
sql = ",".join(sql)

ids = list(sorted(ids))

# criando tabela

cur.execute(f"DROP TABLE IF EXISTS {TABELA};")
cur.execute(f"CREATE TABLE {TABELA} ({sql});")

# coletando tuplas a serem inseridas

tuplas = dict.fromkeys(ids)
for k in tuplas.keys():
	tuplas[k] = dict.fromkeys(cols[1:])

for i, linha in enumerate(linhas):
	linha2 = linha.replace(" ", "")

	if not linha2: # linha em branco, fim do cabeçalho
		break

	vga = linha2.find(",")
	igl = linha2.find("=", vga)

	col = linha2[:vga]
	id_ = int(linha2[vga+1:igl])
	val = int(linha2[igl+1:])

	tuplas[id_][col] = val

# inserindo tuplas

tuplas2 = [
	[str(k)]+[str(val) for val in v.values()]
	for k, v in tuplas.items()
]
sql = ["(" + ",".join(t) + ")" for t in tuplas2]
sql = ",".join(sql)

# sql = []
# for k, v in tuplas.items():
# 	ins = [str(k)]
# 	for val in v.values():
# 		ins.append(str(val))
# 	ins = "(" + ",".join(ins) + ")"
# 	sql.append(ins)
# sql = ",".join(sql)

cur.execute(f"INSERT INTO {TABELA} VALUES {sql};")

tuplas2.insert(0, cols)
tab = Table(tuplas2)
tab.justify_columns = {c: "center" for c, _ in enumerate(cols)}
print("Tabela inicial:")
print()
print(tab.table)
print()

# fechando conexão

cur.close()
con.close()

