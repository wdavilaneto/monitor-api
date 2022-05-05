import math
import sqlite3
from builtins import print

import numpy
import pandas as pd
import psycopg2
import numpy as np
import random
import datetime as dt
from pprint import pprint

from numpy.f2py.auxfuncs import throw_error
from pandas.tseries.offsets import BDay
from sqlalchemy import create_engine


class ProjectImporter:
    """ Class for import data from stadanrd Scrum Datasheet to Database"""

    def __init__(self, nome="SINALID", xls="sinalid.xlsx"):
        # CONNECTION = "dbname='postgres' user='bi' host='d-postgres01.pgj.rj.gov.br' password='bi_des'"
        # ENG_CONNECTION = 'postgresql://bi:bi_des@d-postgres01.pgj.rj.gov.br:5432/postgres'
        CONNECTION = "db.sqlite3"
        ENG_CONNECTION = 'sqlite:///db.sqlite3'

        self.nome = nome
        self.xls = xls
        self.connection = CONNECTION
        self.engine = create_engine(ENG_CONNECTION)
        self.conn = sqlite3.connect(self.connection)  # psycopg2.connect(self.connection)

    def get_connection(self):
        # return self.get_connection()
        return self.conn

    def get_projeto_id(self):
        conn = self.get_connection()
        projeto_id = conn.execute("select p.id from projetos_projeto p where p.nome = ? ", (self.nome,)).fetchone()
        if projeto_id:
            print("Processando projeto '", self.nome, "' (id:", int(projeto_id[0]), ")")
            return int(projeto_id[0])
        else:
            throw_error("Projeto nao encontrado")
        return None

    def execute(self):
        # quick check projeto to exit process in case of error
        projeto_id = self.get_projeto_id()
        # self.process_anotacao(projeto_id)
        self.process_riscos(projeto_id)
        self.process_burnup(projeto_id)
        self.process_backlog(projeto_id)

    def process_anotacao(self, projeto_id):
        conn = cursor = self.get_connection()
        notes = pd.read_excel( self.xls, sheet_name='Notes')
        notes.to_sql('notes', self.engine, if_exists='replace')

        cursor.execute(" delete from projetos_anotacao where projeto_id = ? ", (projeto_id,))
        cursor.execute(" insert into projetos_anotacao ( data, nome, flag, resolvido , projeto_id )"
                       " select date(h.data), h.diario_de_bordo, flag, 0, " + str(projeto_id) + " from notes h")
        conn.commit()
        return projeto_id

    def process_burnup(self, projeto_id):
        conn = cursor = self.get_connection()

        burnup = pd.read_excel( self.xls, sheet_name="Burnup")
        burnup.to_sql('burnup', self.engine, if_exists='replace')

        cursor.execute("delete from burnup where inicio is null or termino is null")
        cursor.execute("delete from projetos_burnup where projeto_id=? ", (projeto_id,))
        cursor.execute(
            " insert into projetos_burnup "
            " (      inicio,termino,iteracao,produzido,acumulado,esforco, entrega, descricao, "
            "        velocidade_pessisimista, velocidade_realista, velocidade_otimista, dias_sprint, projeto_id "
            " ) "
            " select date(inicio),date(termino),iteracao,produzido, acumulado, esforco, entrega, descricao, "
            "        velocidade_pessimista, velocidade_realista, velocidade_otimista, dias_sprint, "
            + str(projeto_id) + " from burnup ")
        conn.commit()

    def process_riscos(self, projeto_id):
        try:
            conn = cursor = self.get_connection()
            burnup = pd.read_excel( self.xls, sheet_name="Riscos")
            burnup.to_sql('riscos', self.engine, if_exists='replace')

            cursor.execute(" delete from projetos_risco where projeto_id=? ", (projeto_id,))
            cursor.execute(" insert into projetos_risco (levantado, nivel, descricao, sugestao, projeto_id) "
                           " select date(levantado), nivel, descricao, sugestao, " + str(projeto_id) +
                           " from riscos ")
            conn.commit()
        except:
            print("Aba de 'Riscos' nao encontrada.")

    def process_backlog(self, projeto_id):
        """
            method to import backlog sheet
        """
        conn = cursor = self.get_connection()

        backlog = pd.read_excel( self.xls, sheet_name="Backlog")
        backlog.to_sql('historia', self.engine, if_exists='replace')
        # cursor.execute("delete from historia where nr is null")

        cursor.execute(" delete from projetos_historia where projeto_id = ?", (projeto_id,))
        # FIXME Baca por causa da falta de padrao das planilhas
        try:
            cursor.execute("insert into projetos_historia "
                           " ( nr, prioridade, pontos, tipo, objetivo, feature, descricao, status, sprint, projeto_id )"
                           " select nr, Prioridade, Esforço, Tipo, Objetivo, Feature, Descrição ,Situação, Iteração, " +
                           str(projeto_id) + " from historia h")
        except:
            cursor.execute("insert into projetos_historia "
                           " ( ID, prioridade, pontos, tipo, objetivo, feature, descricao, status, sprint, projeto_id )"
                           " select ID, Prioridade, Esforço, Tipo, Objetivo, Feature, Descrição ,Situação, Iteração, " +
                           str(projeto_id) + " from historia h")
        conn.commit()

    def update_general_data(self, status, natureza, responsavel, cordenador, lider, velocidade_pactuada):
        conn = psycopg2.connect(self.connection)
        cursor = conn.cursor()
        cursor.execute(" update organograma_projeto "
                       " set status = %s , natureza = %s, responsavel = %s, cordenador = %s , lider = %s  , "
                       " velocidade_pactuada = %s "
                       " where nome = %s "
                       , (status, natureza, responsavel, cordenador, lider, velocidade_pactuada, self.nome))
        conn.commit()

#
# pi = ProjectImporter("SINALID", xls="sinalid.xlsx")
# pi.upsert_burnup()
# pi.update_andamento_projeto()
#
# pi = ProjectImporter("Integra Extrajudicial", xls="extrajudicial.xlsx")
# # pi.extract_genreal_data()
# # pi.upsert_backlog()
# pi.upsert_burnup(usecols="A:G", nrows=14)
