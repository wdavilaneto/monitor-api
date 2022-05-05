from etl.scrum_import import ProjectImporter

pi = ProjectImporter("./resources/Integra Judicial", xls="judicial.xlsx")
pi.execute()

pi = ProjectImporter("./resources/Integra Extrajudicial", xls="extrajudicial2.xlsx")
pi.execute()

# pi = ProjectImporter("MGP", xls="mgp.xlsx")
# pi.execute()
pi = ProjectImporter("./resources/Projeto Casos", xls="ouvidoria.xlsx")
pi.execute()
pi = ProjectImporter("./resources/Integra Polícia Civil", xls="policial.xlsx")
pi.execute()
# pi = ProjectImporter("INTEGRA BUSCA", xls="busca.xlsx")
# pi.execute()
# pi = ProjectImporter("SINALID", xls="sinalid.xlsx")
# pi.execute()
# pi = ProjectImporter("Integra Judicial – Procuradorias", xls="integra_implnatacao.xlsx")
# pi.execute()
