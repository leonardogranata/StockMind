from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("cadastro/", views.cadastroUser, name="cadastro"),
    path("logout/", views.logoutUser, name="logout"),
    path("listar/", views.listarUsers, name="listar"),
    path("editar/<int:user_id>/", views.editarUser, name="editar"),
    path("excluir/<int:user_id>/", views.excluirUser, name="excluir"),
]
