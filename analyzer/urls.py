from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
