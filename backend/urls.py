"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from backend.views import UserViewSet, GroupViewSet

from portfolio.views import *

from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'board', BoardViewSet)
router.register(r'task', TaskViewSet)
router.register(r'objective', ObjectiveViewSet)
router.register(r'keyresult', KeyResultsViewSet)
router.register(r'keyresultvalue', KeyResultValueViewSet)
# router.register(r'login', LoginView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', views.index, name='index'),
    path('portfolio/', include('portfolio.urls')),
    # path('demandas/', include('demandas.urls')),
    # path('pessoas/', include('pessoas.urls')),
    # path('projetos/', include('projetos.urls')),

]
