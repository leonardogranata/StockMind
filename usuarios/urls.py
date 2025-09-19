from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("cadastro/", views.cadastroUser, name="cadastro"),
]
