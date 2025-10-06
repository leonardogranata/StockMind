from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Estoque(models.Model):
    codigo = models.CharField(max_length=25)
    nome = models.CharField(max_length=100, default='Sem nome')
    descricao = models.TextField()
    quantidade = models.IntegerField()
    marca = models.CharField(max_length=120)
    fornecedor = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    qtd_min = models.IntegerField()
    qtd_max = models.IntegerField()

    def __str__(self):
        return self.nome

class Auditoria(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    tabela = models.CharField(max_length=50)
    acao = models.CharField(max_length=10)  # INSERT, UPDATE, DELETE
    registro_id = models.IntegerField()
    data_hora = models.DateTimeField(default=timezone.now)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.acao} em {self.tabela} - ID {self.registro_id}"

    class Meta:
        db_table = 'estoque_auditoria'  # força o nome da tabela
