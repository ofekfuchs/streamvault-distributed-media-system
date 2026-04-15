from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('QueryResults', views.QueryResults, name='QueryResults'),
    path('RecordsManagement', views.RecordsManagement, name='RecordsManagement'),
    path('Rankings', views.Rankings, name='Rankings'),
    path('returnOrder', views.returnOrder, name='returnOrder'),
]
