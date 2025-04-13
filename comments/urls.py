from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_comment, name='add_comment'),
    path('get/', views.get_comments, name='get_comments'),
] 