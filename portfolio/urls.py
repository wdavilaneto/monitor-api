from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    # path('', views.index, name='index'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    path('bsr/', views.get_bsr),
    path('bsr/<int:id>/', views.get_bsr_by_id),
    # path('all/', views.find_all_project(), name='all_projetos_with'),
    # path('bsr/<int:id>/', views.BoardStatisticsResource.as_view()),
]
