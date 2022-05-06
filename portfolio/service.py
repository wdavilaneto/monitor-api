import logging
import os
from pprint import pprint

from trello import TrelloClient

from backend.settings import API_KEY, API_SECRET, TOKEN, TOKEN_SECRET


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
    if not API_KEY:
        API_KEY = os.environ.get('API_KEY')
    if not API_SECRET:
        API_SECRET = os.environ.get('API_SECRET')
    if not TOKEN:
        TOKEN = os.environ.get('TOKEN')
    if not TOKEN_SECRET:
        TOKEN_SECRET = os.environ.get('TOKEN_SECRET')

