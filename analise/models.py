from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from estoque.models import Estoque

class Consumo(models.Model):
    item = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    data = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item.nome} - qtd: {self.quantidade} ({self.data})"
