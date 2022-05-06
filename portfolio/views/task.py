from rest_framework import viewsets, serializers
from url_filter.integrations.drf import DjangoFilterBackend
from url_filter.filtersets import ModelFilterSet
from portfolio.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1


class TaskFilterSet(ModelFilterSet):
    class Meta(object):
        model = Task


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = TaskFilterSet
