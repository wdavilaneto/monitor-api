from rest_framework import views
from rest_framework import serializers
from rest_framework.response import Response


class TrelloSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    comments = serializers.IntegerField()
    likes = serializers.IntegerField()


class TrelloViewSet(views.APIView):
    def get(self, request):
        yourdata = [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
        results = TrelloSerializer(yourdata, many=True).data
        return Response(results)
