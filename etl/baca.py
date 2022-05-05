import psycopg2
import pandas as pd

import datetime

# con = sqlite3.connect('../mysite/sqlite3.db')
# return psycopg2.connect(
#     "dbname='sgfmqpzj' user='sgfmqpzj' host='elmer.db.elephantsql.com' password='YrB-Ge294Cn9buQQGD665hSUbZaCRy9Y'")
con = psycopg2.connect("dbname='postgres' user='bi' host='d-postgres01.pgj.rj.gov.br' password='bi_des'")

cursor = con.cursor()


def insert_secretario():
    cursor.execute("insert into organograma_orgao "
                   "(sigla, nome, texto , responsavel ,funcao, local,  telefone, email)"
                   "values (? , ? , ? , ? ,?, ? ,? ,?) ",
                   (
                       'STIC', 'SECRETARIA DE TECNOLOGIA DA INFORMAÇÃO E DE COMUNICAÇÃO', '',
                       'SANDRO DENIS DE SOUZA NUNES',
                       'SECRETÁRIO DE TI',
                       'Av. Marechal Camara 370', '(21) 2222-2222', 'sandro.nunes@mprj.mp.br'
                   ))
    # cursor.commit()

