from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.cadastroItem, name="cadastroItem"),
    path("editar/<int:pk>/", views.editarItem, name="editarItem"),
    path("excluir/<int:pk>/", views.excluirItem, name="excluirItem"),
    path("auditoria/", views.auditoria_list, name="auditoria_list"),
    path('exportar/', views.exportar_json, name='exportar_json'),
    path('importar/', views.importar_json, name='importar_json'),
]
