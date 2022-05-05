import json
from datetime import datetime, timedelta
from pprint import pprint

from django.http import JsonResponse
from django_pandas.io import read_frame
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from sqlalchemy import and_
from url_filter.integrations.drf import DjangoFilterBackend
from url_filter.filtersets import ModelFilterSet
from .models import Task, Board, Objective, KeyResults, KeyResultValue
from django.db import connection

from rest_framework.response import Response
from rest_framework import status

import pandas as pd


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


def get_bsr(request):
    labels = []
    with connection.cursor() as cursor:
        cursor.execute("Select distinct label from portfolio_task")
        for row in cursor.fetchall():
            labels.append(row[0])

    date_limit = datetime.today() - timedelta(days=120)
    sql = """ 
    select count(*), TO_CHAR(friday, 'DD/MM/YYYY') , label from portfolio_task 
    where friday >= %s
    group by friday, label 
    order by friday """
    result = []
    with connection.cursor() as cursor:
        cursor.execute(sql, [date_limit])
        for row in cursor.fetchall():
            result.append(
                {'friday': row[1], 'label': row[2], 'count': row[0]}
            )
    return JsonResponse({'labels': labels, 'results': result}, safe=False)


def get_bsr_by_id(request, id):
    labels = []
    with connection.cursor() as cursor:
        cursor.execute("Select distinct label from portfolio_task")
        for row in cursor.fetchall():
            labels.append(row[0])

    date_limit = datetime.today() - timedelta(days=150)
    sql = """ 
    select count(*), TO_CHAR(friday, 'DD/MM/YYYY') , label from portfolio_task 
    where board_id = %s and friday >= %s   group by friday, label   order by friday """
    result = []
    total = 0
    with connection.cursor() as cursor:
        cursor.execute(sql, [id, date_limit])
        for row in cursor.fetchall():
            result.append(
                {'friday': row[1], 'label': row[2], 'count': row[0]}
            )
            total += row[0]
    return JsonResponse({'labels': labels, 'results': result, 'total': total}, safe=False)




# class BoardStatisticsResource(APIView):
    # def put(self, request, id=None):
    # result = df.groupby('label')['cycle_time'].agg(['sum', 'count', 'mean', 'median'])



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
