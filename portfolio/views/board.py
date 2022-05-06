from rest_framework import viewsets, serializers
from url_filter.integrations.drf import DjangoFilterBackend
from url_filter.filtersets import ModelFilterSet
from portfolio.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        depth = 1


class BoardFilterSet(ModelFilterSet):
    class Meta(object):
        model = Board


class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = BoardFilterSet
