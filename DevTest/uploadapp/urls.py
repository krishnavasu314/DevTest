# from django.htpp import request
from django.urls import path
from . import views
 

urlpatterns=[
    path('', views.upload_file_view, name='upload_file'),
    path('result/', views.sucess, name='sucess'),
    ]
