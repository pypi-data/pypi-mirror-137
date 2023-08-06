from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('form/', views.FormView.as_view(), name='form'),
    path('modal/', views.modal, name='modal'),
    path('table/', views.table, name='table'),
    path('table/filtered/', views.FilteredTable.as_view(), name='filtered-table'),
]

app_name = 'backend'
