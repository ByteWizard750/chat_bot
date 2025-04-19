from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Either replace this line with the one below or remove it
    # path('article/', views.article, name='article'),
    path('article/', views.index, name='article'),  # Reuse index view for article URL
]