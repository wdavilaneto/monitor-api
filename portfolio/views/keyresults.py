from rest_framework import viewsets, serializers
from url_filter.integrations.drf import DjangoFilterBackend
from url_filter.filtersets import ModelFilterSet
from portfolio.models import KeyResults, KeyResultValue


class KeyResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResults
        fields = '__all__'
        depth = 1


class KeyResultsFilterSet(ModelFilterSet):
    class Meta(object):
        model = KeyResults


class KeyResultsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KeyResults.objects.all()
    serializer_class = KeyResultsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = KeyResultsFilterSet

class KeyResultValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResultValue
        fields = '__all__'
        depth = 1


class KeyResultValueFilterSet(ModelFilterSet):
    class Meta(object):
        model = KeyResultValue


class KeyResultValueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KeyResultValue.objects.all()
    serializer_class = KeyResultValueSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = KeyResultValueFilterSet