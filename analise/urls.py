from django.urls import path
from . import views

urlpatterns = [
    path('previsao/<str:item_nome>/', views.previsao_view, name='previsao'),
]
