# Copyright © 2021 Paulo Gabriel Sena Comasetto <paulogscomasetto@gmail.com>


import argparse
import re

import psycopg2 as psql
from terminaltables import AsciiTable as Table


# obtendo argumentos da linha de comando

psr = argparse.ArgumentParser(
	description="Programa para execução de log REDO."
)

psr.add_argument("arquivo") # caminho do arquivo, obrigatório
psr.add_argument("--banco", default="log") # opcional
psr.add_argument("--usuario", default="postgres") # opcional
psr.add_argument("--senha", default="postgres") # opcional

args = psr.parse_args()
