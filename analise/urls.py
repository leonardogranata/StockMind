from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('dashboard/previsao/', views.previsao, name='previsao'),
    path('dashboard/mais-usados/', views.itens_mais_usados, name='mais_usados'),
    path('dashboard/maquinas/', views.dashboard_maquinas, name='dashboard_maquinas'),
]