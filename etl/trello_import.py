from trello import TrelloClient

chave = '73c5f28f57d0e270a2065be0d92bed53'
secret = 'f1518798df8746d2a57e83e872b979c28d79ef40edaafa3d994a1b281666f728'
token = 'b68d6f1834ce1e73f8ec7de5e7a15f76fd2406629c3af8899db3ba3a75968de6'
oauth_toke_secret = 'f1518798df8746d2a57e83e872b979c28d79ef40edaafa3d994a1b281666f728'

client = TrelloClient(
    api_key=chave,
    api_secret=secret,
    token=token,
    token_secret=oauth_toke_secret
)

# all_boards = client.list_boards()
# for board in all_boards:
#     print( (board, board.id) )

dti_projetos = '5c46304f7ee6885f8260c82c'
gsi_coordenacao = '5ad10d8422b0bde84e3164af'
dti = '5c86e4bfd335f03ca864e23f'
dti_rh = '5a0b3c10a8fa1c164e9eb53b'
integra_ip_ready = '5cae28f93c177284d1d0a746'

specific = client.get_board(dti)

for list in specific.list_lists():
    print(list.name, list, list.id)
    for card in list.list_cards():
        print("   ->", card.name, card.id)
