from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from url_filter.integrations.drf import DjangoFilterBackend
# from urllib3.packages.rfc3986.compat import unicode

from backend.serializers import UserSerializer, GroupSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Create your views here.
def index(request):
    return HttpResponse("This is a protected GSI api backend")

#
# class LoginView(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_class = UserViewSet
#
#     def get(self, request, format=None):
#         content = {
#             'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#             'auth': unicode(request.auth),  # None
#         }
#         return Response(content)
