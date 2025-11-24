from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Estoque(models.Model):
    codigo = models.CharField(max_length=25)
    nome = models.CharField(max_length=25, default='Sem nome')
    descricao = models.TextField()
    quantidade = models.IntegerField()
    marca = models.CharField(max_length=25)
    fornecedor = models.CharField(max_length=25)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    qtd_min = models.IntegerField()
    qtd_max = models.IntegerField()

    def __str__(self):
        return self.nome

class Maquina(models.Model):
    codigo = models.CharField(max_length=25, unique=True)
    nome = models.CharField(max_length=25)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=25, blank=True)
    data_aquisicao = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Ativa', 'Ativa'),
            ('Em manutenção', 'Em manutenção'),
            ('Inativa', 'Inativa'),
        ],
        default='Ativa'
    )
    pecas = models.ManyToManyField(Estoque, related_name='maquinas')

    def __str__(self):
        return self.nome


class Auditoria(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    tabela = models.CharField(max_length=25)
    acao = models.CharField(max_length=10)
    registro_id = models.IntegerField()
    data_hora = models.DateTimeField(default=timezone.now)
    descricao = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.acao} em {self.tabela} - ID {self.registro_id}"

    class Meta:
        db_table = 'estoque_auditoria'
