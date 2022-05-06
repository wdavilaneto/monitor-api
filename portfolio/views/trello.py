from rest_framework import views
from rest_framework import serializers
from rest_framework.response import Response
from trello import TrelloClient

from backend.settings import API_KEY, API_SECRET, TOKEN, TOKEN_SECRET
from portfolio.service import TrelloService

EXCLUSIONS = ["5d767a3dd9cb604a49ab3e87", "5771ab243af6f7e04efdaa98", "537caf550a5e749e488d9f9b",
              "593ed2858fbda5bf0bf24ca2", "58c69e02ac1f89e706448fe8", "5e3da47c321ff76844b99eff",
              "5c46304f7ee6885f8260c82c", "5fbd0ba047715155295f4812", "5fbbb88219d8b90a3af1641a",
              "5fd2bcadaab6195dc1284d40", ""]


class TrelloSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    name = serializers.StringRelatedField()
    id = serializers.StringRelatedField()
    url = serializers.StringRelatedField()
    description = serializers.StringRelatedField()


class TrelloViewSet(views.APIView):

    def __init__(self):

        self.client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN,
            token_secret=TOKEN_SECRET
        )

    def get(self, request):
        output = []
        all_boards = self.client.list_boards()
        for board in all_boards:
            if board.id not in EXCLUSIONS:
                if not board.closed:
                    output.append(
                        {"name": board.name, "id": board.id, "url": board.url, "description": board.description})

        results = TrelloSerializer(output, many=True).data
        return Response(results)
