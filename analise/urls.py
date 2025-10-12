from django.urls import path
from . import views

urlpatterns = [
    path('previsao/', views.previsao, name='previsao'),
]