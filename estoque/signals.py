from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Estoque, Auditoria

@receiver(post_save, sender=Estoque)
def estoque_auditoria(sender, instance, created, **kwargs):
    acao = 'INSERT' if created else 'UPDATE'

    descricao = (
        f"Item {'criado' if created else 'atualizado'}.\n"
        f"Código: {instance.codigo}\n"
        f"Nome: {instance.nome}\n"
        f"Quantidade: {instance.quantidade}\n"
        f"Marca: {instance.marca}\n"
        f"Fornecedor: {instance.fornecedor}\n"
        f"Preço: {instance.preco}\n"
        f"Qtd Mínima: {instance.qtd_min}\n"
        f"Qtd Máxima: {instance.qtd_max}"
    )

    Auditoria.objects.create(
        tabela='Estoque',
        acao=acao,
        registro_id=instance.id,
        descricao=descricao
    )

@receiver(post_delete, sender=Estoque)
def estoque_auditoria_delete(sender, instance, **kwargs):
    descricao = (
        "Item deletado.\n"
        f"Código: {instance.codigo}\n"
        f"Nome: {instance.nome}"
    )

    Auditoria.objects.create(
        tabela='Estoque',
        acao='DELETE',
        registro_id=instance.id,
        descricao=descricao
    )
