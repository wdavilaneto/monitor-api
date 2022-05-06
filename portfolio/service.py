import logging
from pprint import pprint

from trello import TrelloClient

from config import Config


def guess_label(labels):
    if labels:
        for label in labels:
            if 'histo' in label.name.lower() or 'funcion' in label.name.lower():
                return 'História'
            if 'erro' in label.name.lower() or 'corre' in label.name.lower():
                return 'Correção'
            if 'manut' in label.name.lower() or 'ajuste' in label.name.lower():
                return 'Ajuste'
            if 'oper' in label.name.lower():
                return 'Operação'
            if 'débito' in label.name.lower() or 'tarefa técnica' in label.name.lower():
                return 'Débito'
            if 'atendi' in label.name.lower() or 'suporte' in label.name.lower():
                return 'Atendimento'
    return 'Outros'


class TrelloService():
    EXTRAJUDICIAL = '5e3855eded3f7a0152dcc387'
    POLICIAL = '5f0dd7789edaca5954e380e0'
    JUDICIAL = '5d41e061295f5a0e31734864'
    INTGEGRACAO = '5b9975423903482aae3259dd'
    MGP = '5e8b3a4c7c9f961b3111ccbc'
    PRATICAS_AGEIS = '5e4ed9c99251e6193b445f96'
    MANUTENCOES = '5e39bc58a43cdd342c32383e'
    RH = '5ef0c4c76fed946daced33e0'
    RH_WEB = '5ef12720704eec7e1e4c27e0'
    SINALID = '5de7ec8722433a8a634fe998'
    NAO_FUNCIONAIS = '5e4ecd2b47fc95248bd39d36'
    INTEGRACAO = '5b9975423903482aae3259dd'

    def __init__(self):
        config = Config()
        self.client = TrelloClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            token=config.TOKEN,
            token_secret=config.TOKEN_SECRET
        )
        logging.info("TRello API Key " + config.API_KEY)

    def list_boards(self):
        output = []
        all_boards = self.client.list_boards()
        for board in all_boards:
            if board.id not in ["5d767a3dd9cb604a49ab3e87", "5771ab243af6f7e04efdaa98", "537caf550a5e749e488d9f9b"]:
                output.append({"name": board.name, "id": board.id})
        return output


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=1)
    ts = TrelloService()
    pprint(ts.list_boards())
    # print(ts.get("5d41e061295f5a0e31734864"))
    # ts.test()
