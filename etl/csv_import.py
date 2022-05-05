import pandas as pd
import psycopg2
import random
import datetime
from pprint import pprint
import yaml


def connect(database='gestao'):
    if (database == 'gestao'):
        config = yaml.load(open('config.yaml', 'r'))
        pg_conn = psycopg2.connect(config['data']['postgres']['uri'])
        cursor = pg_conn.cursor()
        print (pg_conn, cursor)
        return pg_conn, cursor
    else:
        from sqlite3 import Error
        import sqlite3
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect("db.sqlite3")
            return conn, conn
        except Error as e:
            print(e)
        return None


def fix_orgaos(excel):
    pg_conn = connect()
    cursor = pg_conn  # pg_conn.cursor()

    print(excel)
    for i, row in excel.iterrows():
        orgao = str(row['orgao']).strip()
        login = str(row['login']).strip()
        cursor.execute(
            "UPDATE orgaos_orgao SET responsavel_id = (select id from pessoas_pessoa where login = %s ) "
            "where sigla = %s ", (login, orgao))
    pg_conn.commit()


def cadastra_sistemas(sistemas):
    print(sistemas)
    pg_conn, cursor = connect()
    for i, row in sistemas.iterrows():
        sigla = str(row['sigla']).strip()
        nome = str(row['nome']).strip()
        descricao = str(row['descricao']).strip()
        tipo = str(row['tipo']).strip()
        status = str(row['status']).strip()
        custo = str(row['Custo']).strip()
        # try:
        r = cursor.execute("select count(*) from projetos_sistema where sigla = %s", (sigla,)).fetchall()
        if r[0][0] is 0:
            cursor.execute(
                " INSERT INTO projetos_sistema (sigla, nome, descricao , tipo , status, custo ) "
                " values ( %s,%s,%s,%s,%s,%s ) "
                , (sigla, nome, descricao, tipo, status, custo))
        else:
            cursor.execute(
                " UPDATE projetos_sistema set nome =%s , descricao =%s , tipo= %s , status= %s , custo =%s  "
                " WHERE sigla = %s "
                , (nome, descricao, tipo, status, custo, sigla))
        # , (key, datetime.datetime.now(), tipo, status, value['texto'], value['lotacao'],))
        # except:
        #     print('key already exists')

    pg_conn.commit()


def cadastra_projetos(projetos):
    print(projetos)
    pg_conn = connect()
    cursor = pg_conn  # pg_conn.cursor()
    for i, row in projetos.iterrows():
        nome = str(row['nome']).strip()
        descricao = str(row['descricao']).strip()
        status = str(row['status']).strip()
        andamento = int(row['andamento'])
        po = str(row['po']).strip()
        custo = row['custo_total']
        cordenador_id = str(row['cordenador_id']).strip()
        lider_id = str(row['lider_id']).strip()
        orgao_id = str(row['orgao_id']).strip()
        sistema = row['sistema']
        tipo = str(row['tipo']).strip()

        r = cursor.execute("select count(*) from projetos_projeto where nome = %s", (nome,)).fetchall()
        if r[0][0] is 0:
            cursor.execute(
                " INSERT INTO projetos_projeto (nome, descricao , status, andamento, po , custo, cordenador_id, lider_id, orgao_id, sistema_id, ultima_atualizacao, tipo ) "
                " values ( %s, %s , %s, %s, %s , %s, %s, "
                " (select id from pessoas_pessoa where login = %s), "
                " (select id from pessoas_pessoa where login = %s), "
                " (select id from orgaos_orgao where sigla = %s), "
                " (select id from projetos_sistema where sigla = %s), "
                " %s, %s )"
                , (nome, descricao, status, andamento, po, custo, cordenador_id, lider_id, orgao_id, sistema,
                   datetime.datetime.now(), tipo))
        else:
            cursor.execute(
                " UPDATE projetos_projeto set descricao = %s , status= %s , andamento = %s, po =%s , custo =%s, "
                " cordenador_id= (select id from pessoas_pessoa where login = %s), "
                " lider_id = (select id from pessoas_pessoa where login = %s) , "
                " orgao_id = (select id from orgaos_orgao where sigla = %s) , "
                " sistema_id = (select id from projetos_sistema where sigla = %s), "
                " ultima_atualizacao = %s, tipo = %s where nome = %s"
                , (descricao, status, andamento, po, custo, cordenador_id, lider_id, orgao_id, sistema,
                   datetime.datetime.now(), tipo, nome))
        # except:
        #     print('key already exists')

    pg_conn.commit()


def cadastra_papeis(papeis):
    print(papeis)
    pg_conn = connect()
    cursor = pg_conn  # pg_conn.cursor()
    for i, row in papeis.iterrows():
        nome = str(row['nome']).strip()
        descricao = str(row['descricao']).strip()
        tipo = str(row['tipo']).strip()
        orgao = str(row['orgao']).strip()
        r = cursor.execute("select count(*) from pessoas_papel where nome = %s", (nome,)).fetchall()
        if r[0][0] is 0:
            cursor.execute(" INSERT INTO pessoas_papel (nome, descricao, tipo, orgao_id ) values "
                           " ( %s, %s, %s, (select id from orgaos_orgao where sigla = %s)  )"
                           , (nome, descricao, tipo, orgao))
        else:
            cursor.execute(" UPDATE pessoas_papel set descricao = %s , tipo= %s, "
                           " orgao_id = (select id from orgaos_orgao where sigla = %s) "
                           " where nome = %s "
                           , (descricao, tipo, orgao, nome,))
    cursor.commit()


def cadastra_cargos(cargo):
    print(cargo)
    cursor = pg_conn = connect()
    for i, row in cargo.iterrows():
        nome = str(row['nome']).strip()
        valor = str(row['valor']).strip()
        r = cursor.execute("select count(*) from pessoas_cargo where nome = %s", (nome,)).fetchall()
        if r[0][0] is 0:
            cursor.execute(" INSERT INTO pessoas_cargo (nome, valor) values ( %s, %s  )", (nome, valor))
        else:
            cursor.execute(" UPDATE pessoas_cargo set valor = %s where nome = %s ", (valor, nome,))
    cursor.commit()


def relaciona_pessoas(pessoas):
    print(pessoas)
    cursor = pg_conn = connect()
    for i, row in pessoas.iterrows():
        login = str(row['login']).strip()
        papel = str(row['papel']).strip()
        cargo = str(row['cargo']).strip()
        estatutario = int(row['estatutario'])
        orgao = str(row['orgao']).strip()
        r = pg_conn.execute("select count(*) from pessoas_pessoa where login = %s", (login,)).fetchall()
        if r[0][0] is 0:
            print(login, " NAO Encontrado!!!")
        else:
            pg_conn.execute(" UPDATE pessoas_pessoa set "
                            " papel_id  = (select id from pessoas_papel where nome = %s) , "
                            " cargo_id  = (select id from pessoas_cargo where nome = %s) , "
                            " orgao_id  = (select id from orgaos_orgao where sigla = %s) , "
                            " estatutario = %s "
                            " where login = %s "
                            , (papel, cargo, orgao, estatutario, login,))
    cursor.commit()


file = "./resources/gestao.xlsx"
# fix_orgaos(pd.read_excel(file, sheet_name="organograma"))
cadastra_sistemas(pd.read_excel(file, sheet_name="sistemas"))
cadastra_projetos(pd.read_excel(file, sheet_name="projetos"))
cadastra_papeis(pd.read_excel(file, sheet_name="papeis"))
cadastra_cargos(pd.read_excel(file, sheet_name="cargos"))
relaciona_pessoas(pd.read_excel(file, sheet_name="pessoas"))
