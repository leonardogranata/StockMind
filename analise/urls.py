from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('previsao/', views.previsao, name='previsao'),
    path('mais-usados/', views.itens_mais_usados, name='mais_usados'),
]