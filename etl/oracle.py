""" Module to export connection to Oracle...."""
import os, sys

import cx_Oracle

# you may need somthing like: ln -s libclntsh.so.12.1 libclntsh.so
# remember to instal libaio-dev (apt-get)
# export LD_LIBRARY_PATH=/opt/oracle/instantclient_12_2:$LD_LIBRARY_PATH ..or on ldconf.d etc,etc
os.putenv('LD_LIBRARY_PATH', '/opt/oracle/')
__oracle_instance = None

def oracle_connection():
    global __oracle_instance
    if __oracle_instance is None:
        fp = open("oracle.pass", 'r')
        passwd = fp.read()
        fp.close()
        __oracle_instance = cx_Oracle.connect( passwd + '@exa-scan.pgj.rj.gov.br:1521/corr', encoding='utf-8')
        #_oracle_instance = cx_Oracle.connect('walter/a123@exa-scan.pgj.rj.gov.br:1521/desenv', encoding='utf-8')
        print("oracle connection: ", __oracle_instance.version)
        print(__oracle_instance.encoding)
    return __oracle_instance


def __execute_sql_file(filename, numRows=None):
    interess_arq_sqlfile = open(filename, 'r')
    arq_sql = interess_arq_sqlfile.read()
    interess_arq_sqlfile.close()
    cursor = oracle_connection().cursor()
    cursor.execute(arq_sql)
    if numRows is None:
        return cursor
    result = cursor.fetchmany(numRows=numRows)
    cursor.close()
    return result


def __execute_paged_sql_file(filename, first=0, last=10):
    interess_arq_sqlfile = open(filename, 'r')
    arq_sql = interess_arq_sqlfile.read()
    interess_arq_sqlfile.close()
    cursor = oracle_connection().cursor()
    cursor.execute(arq_sql, [first, last])
    result = cursor
    return result


def find_arq(numRows=None):
    return __execute_sql_file('../resources/sql/arq.sql', 'r')


def find_personagem_documento(numRows=None):
    return __execute_sql_file('../resources/sql/personagem_documento.sql', 'r')


def find_all_comunicacoes():
    return __execute_sql_file('../resources/sql/ouvidoria_find_comunicacao.sql')


def get_comunicacao(id):
    return __execute_sql_file('../resources/sql/ouvidoria_find_comunicacao.sql')


def rows_as_dicts(cursor):
    """ returns cx_Oracle rows as dicts """
    colnames = [i[0] for i in cursor.description]
    # print (colnames)
    for row in cursor:
        yield dict(zip(colnames, row))


if __name__ == '__main__':
    """Test connection"""
    print(__doc__)
    oracle_connection()
    # for row in find_personagem_documento(30):
    # for row in find_arq(3):
    #     print(row)
    # for row in find_all_comunicacoes():
    #     print(row)
