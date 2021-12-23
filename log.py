# Copyright © 2021 Paulo Gabriel Sena Comasetto <paulogscomasetto@gmail.com>


import argparse
import re

import psycopg2 as psql
from terminaltables import SingleTable as Table


TABELA = "log" # tabela única do banco


def imprimirTabela():
	cons = [tuple(cols)]
	cur.execute(f"SELECT * FROM {TABELA} ORDER BY id;")
	cons.extend(cur.fetchall())
	tab = Table(cons)
	tab.justify_columns = {c: "center" for c, _ in enumerate(cols)}
	print(tab.table)


# obtendo argumentos da linha de comando

psr = argparse.ArgumentParser(
	description="Programa para execução de log REDO."
)

psr.add_argument("arquivo") # caminho do arquivo, obrigatório
psr.add_argument("--banco", default="log") # opcional
psr.add_argument("--usuario", default="postgres") # opcional
psr.add_argument("--senha", default="postgres") # opcional

args = psr.parse_args()

# --- 1) PARTE INICIAL

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

# --- 2) CRIAÇÃO E INSERÇÃO NA TABELA

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

ids = sorted(ids)

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

del linhas[:i+1] # deleta cabeçalho

# inserindo tuplas

tuplas2 = [
	[str(k)]+[str(val) for val in v.values()]
	for k, v in tuplas.items()
]
sql = ["(" + ",".join(t) + ")" for t in tuplas2]
sql = ",".join(sql)

cur.execute(f"INSERT INTO {TABELA} VALUES {sql};")

# imprimindo tabela inicial

print()
print("Tabela inicial:")
imprimirTabela()

# --- 2) BUSCA PELAS TRANSAÇÕES QUE SOFRERAM REDO

# busca pelo último checkpoint efetivado (<end ckpt>)
# a busca é feita de trás para frente

achou_end = False
for i in reversed(range(len(linhas))):
	if linhas[i].lower().startswith("<end"): # <end ckpt>
		achou_end = True
	elif re.search(r"^<start (ckpt|checkpoint)", linhas[i], re.I):
		if achou_end:
			break

# busca por transações que (não) sofrem REDO

if not achou_end:
	secao = linhas[:] # seção de busca
	n_redo = [] # transações em aberto
else:
	secao = linhas[i+1:] # a partir do último ckpt válido
	ap = linhas[i].find("(")
	fp = linhas[i].rfind(")")
	n_redo = linhas[i][ap+1:fp].replace(" ", "").split(",")

redo = [] # transações commitadas
for linha in secao:
	# <start Tn>: adiciona Tn na lista de n_redo
	# <commit Tn>: retira de n_redo e coloca em redo
	if re.search(r"^<start \w+>$", linha, re.I): # <start Tn>
		trans = linha[linha.find(" ")+1:linha.rfind(">")]
		n_redo.append(trans)
	elif re.search(r"<commit \w+>$", linha, re.I): # <commit Tn>
		trans = linha[linha.find(" ")+1:linha.rfind(">")]
		n_redo.remove(trans)
		redo.append(trans)

print()
print(f"Transações que não sofrem REDO: [{','.join(n_redo)}]")
print(f"Transações que sofrem REDO: [{','.join(redo)}]")

# --- 3) SINCRONIZAÇÃO DO LOG COM O BANCO

# busca por alterações commitadas, e atualiza na tabela
# a busca é feita sequencialmente
# critério: transação não pode estar na lista 'n_redo'

nl = False
for linha in linhas:
	linha2 = linha.replace(" ", "")[1:-1]
	if re.search(r"^\w+,\w+,\w+,\w+$", linha2):
		trans, id_, col, val = linha2.split(",")
		if trans not in n_redo: # critério satisfeito
			cur.execute(f"""
				UPDATE {TABELA}
				SET {col}=(%s)
				WHERE id=(%s);""",
				(val, id_)
			)
			if not nl:
				print()
				nl = True
			print(f"Atualizando {col}={val} onde id={id_}")

# imprimindo tabela final

print()
print("Tabela final:")
imprimirTabela()

print()

# --- 4) FECHAMENTOS

cur.close()
con.close()
