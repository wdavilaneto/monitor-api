from etl.oracle import oracle_connection
import psycopg2


# CONNECTION_URL= "dbname='sgfmqpzj' user='sgfmqpzj' host='elmer.db.elephantsql.com' password='YrB-Ge294Cn9buQQGD665hSUbZaCRy9Y'"
# CONNECTION_URL= "dbname='postgres' user='bi' host='d-postgres01.pgj.rj.gov.br' password='bi_des'"

# postgres_conection = psycopg2.connect(
#     "dbname='sgfmqpzj' user='sgfmqpzj' host='elmer.db.elephantsql.com' password='YrB-Ge294Cn9buQQGD665hSUbZaCRy9Y'")

# pg_conn = psycopg2.connect(CONNECTION_URL)
# stic_db = pg_conn.cursor()

def create_connection():
    from sqlite3 import Error
    import sqlite3
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect("db.sqlite3")
        return conn
    except Error as e:
        print(e)
    return None


stic_db = create_connection()

oracle_cursor = oracle_connection().cursor()

funcionarios_sql = """ select RE.RREP_CDMATRICULA_FUNCIONARIO MATRICULA,
            fu.E_MAIL1 login,  RE.RREP_NOME nome, F.FOTO ,
            RE.RREP_NMORGAO orgao, RE.RREP_NMCARGO cargo, RE.RREP_LIQUIDO salario 
        from RH_REMUNERACAO_PT re join RH_FUNCIONARIO fu ON RE.RREP_CDMATRICULA_FUNCIONARIO = Fu.CDMATRICULA
        left join RH_FUNC_IMG f on RE.RREP_CDMATRICULA_FUNCIONARIO = F.CDMATRICULA
        where to_date(RE.RREP_MES_ANO_PAGTO,	'mmyyyy') = (select max( add_months(to_date(RE2.RREP_MES_ANO_PAGTO, 'mmyyyy'), -2))
            from RH_REMUNERACAO_PT re2) and RE.RREP_NUM_PENSAO = 0 and FU.CDORGAO in 
            (SELECT distinct OO.ORGI_CDORGAO FROM ORGI_ORGAO oo WHERE oo.ORGI_DK <> 16656011 AND oo.ORGI_DK <> 200884  AND oo.ORGI_DK <> 2521482
             connect BY prior OO.ORGI_Dk = OO.ORGI_ORGI_DK_SUPERIOR start WITH OO.ORGI_DK = 400802 )
        order BY RE.RREP_NMORGAO, RE.RREP_NOME
        """
responsaveis_sql = """ select RE.RREP_CDMATRICULA_FUNCIONARIO MATRICULA, RE.RREP_NOME NOME, RE.RREP_NMORGAO 
                from RH_REMUNERACAO_PT re join RH_FUNCIONARIO fu ON RE.RREP_CDMATRICULA_FUNCIONARIO = Fu.CDMATRICULA
                left join RH_FUNC_IMG f on RE.RREP_CDMATRICULA_FUNCIONARIO = F.CDMATRICULA
                where to_date(RE.RREP_MES_ANO_PAGTO,	'mmyyyy') = (select max( add_months(to_date(RE2.RREP_MES_ANO_PAGTO, 'mmyyyy'), -2))
            from RH_REMUNERACAO_PT re2) and RE.RREP_NUM_PENSAO = 0 and FU.CDORGAO in 
            (SELECT distinct OO.ORGI_CDORGAO FROM ORGI_ORGAO oo WHERE oo.ORGI_DK <> 16656011 AND oo.ORGI_DK <> 200884  AND oo.ORGI_DK <> 2521482
             connect BY prior OO.ORGI_Dk = OO.ORGI_ORGI_DK_SUPERIOR start WITH OO.ORGI_DK = 400802 )
            AND Fu.CDMATRICULA IN (00007349,00006984, 00006276 , 00007774, 00198228, 08005075, 00003612, 00006419, 00004328,00002235)
            order BY RE.RREP_NMORGAO, RE.RREP_NOME
        """

orgaos_sql = """
            SELECT DISTINCT 
                LEVEL , OO.ORGI_NM_ORGAO ,  OO.ORGI_SIGLA , ORGI_ORGI_DK_SUPERIOR, oo.ORGI_DK, 
                (SELECT o.ORGI_SIGLA FROM ORGI_ORGAO o WHERE o.orgi_dk = oo.ORGI_ORGI_DK_SUPERIOR) as opai, oo.ORGI_DK
            FROM ORGI_ORGAO oo WHERE oo.ORGI_SIGLA <> 'DCA' AND  oo.ORGI_SIGLA <> 'SUBSTIC' AND  oo.ORGI_SIGLA <> 'GEARQ' AND  oo.ORGI_SIGLA <> 'GECOM' AND  oo.ORGI_SIGLA <> 'CAT' 
                 connect BY prior OO.ORGI_Dk = OO.ORGI_ORGI_DK_SUPERIOR start WITH OO.ORGI_DK = 400802
            ORDER BY LEVEL, ORGI_SIGLA 
    
        """


def import_orgaos():
    oracle_cursor.execute(orgaos_sql)
    for each in oracle_cursor:
        level = each[0]
        nome = each[1]
        sigla = each[2]
        opai = each[5]
        print((nome, sigla, level, opai))
        if level == 1:
            stic_db.execute("INSERT INTO orgaos_orgao (nome, sigla, nivel ) VALUES ( ? , ? , ? ) ",
                            (nome, sigla, level,))
        else:
            stic_db.execute("INSERT INTO orgaos_orgao (nome, sigla, nivel , parent_id )"
                            "SELECT  ? , ? , ? , o.id from orgaos_orgao o "
                            "WHERE o.sigla = ? ", (nome, sigla, level, opai))
    stic_db.commit()


def import_funcionarios():
    oracle_cursor.execute(funcionarios_sql)
    for each in oracle_cursor:
        matricula = each[0]
        login = each[1]
        nome = each[2]
        foto = each[3]
        if foto:
            fotostream = foto.read()
        else:
            fotostream = None
        orgao = each[4]
        salario = each[6]

        print(each)
        stic_db.execute(" INSERT INTO pessoas_pessoa (matricula , login , nome, foto, salario)"
                        " values (? ,? , ? , ? , ? )",
                        (matricula, login, nome, fotostream, salario,)
                        )
        stic_db.execute(
            " update pessoas_pessoa set orgao_id = (select id from orgaos_orgao where nome = ? ) where matricula = ? ", (orgao, matricula, )
        )
    stic_db.commit()

def atualiza_salarios():
    oracle_cursor.execute(funcionarios_sql)
    for each in oracle_cursor:
        login = each[1]
        salario = each[6]
        stic_db.execute(
            " update pessoas_pessoa set salario = ? where login = ? ", (salario, login, )
        )
    stic_db.commit()
# ********************************

def import_responsavel():
    oracle_cursor.execute(responsaveis_sql)

    for each in oracle_cursor:
        print(each)
        matricula = each[0]
        nome_orgao = each[2]
        stic_db.execute(
            " UPDATE orgaos_orgao set "
            " responsavel_id = (select id from pessoas_pessoa where matricula = ? ) "
            " where nome = ? ",
            (matricula, nome_orgao))
    stic_db.commit()


# import_orgaos()
# import_funcionarios()
# import_responsavel()
atualiza_salarios()