from rest_framework import viewsets, serializers
from url_filter.integrations.drf import DjangoFilterBackend
from url_filter.filtersets import ModelFilterSet
from portfolio.models import Objective


class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = '__all__'
        depth = 1


class ObjectiveFilterSet(ModelFilterSet):
    class Meta(object):
        model = Objective


class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ObjectiveFilterSet
