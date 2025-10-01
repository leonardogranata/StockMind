from django.db import models

class Estoque(models.Model):
    codigo = models.CharField(max_length=25)
    descricao = models.TextField()
    quantidade = models.IntegerField()
    marca = models.CharField(max_length=120)
    fornecedor = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    qtd_min = models.IntegerField()
    qtd_max = models.IntegerField()

    def __str__(self):
        return self.descricao
