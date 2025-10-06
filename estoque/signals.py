from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Estoque, Auditoria

# Auditoria para Estoque
@receiver(post_save, sender=Estoque)
def estoque_auditoria(sender, instance, created, **kwargs):
    acao = 'INSERT' if created else 'UPDATE'
    descricao = f"Codigo: {instance.codigo}, Nome: {instance.nome}, Quantidade: {instance.quantidade}, Marca: {instance.marca}, Fornecedor: {instance.fornecedor}, Preço: {instance.preco}, Qtd_min: {instance.qtd_min}, Qtd_max: {instance.qtd_max}"
    Auditoria.objects.create(
        usuario=getattr(instance, 'usuario_logado', None),
        tabela='Estoque',
        acao=acao,
        registro_id=instance.id,
        descricao=descricao
    )

@receiver(post_delete, sender=Estoque)
def estoque_auditoria_delete(sender, instance, **kwargs):
    descricao = f"Item deletado: Codigo: {instance.codigo}, Nome: {instance.nome}"
    Auditoria.objects.create(
        usuario=getattr(instance, 'usuario_logado', None),
        tabela='Estoque',
        acao='DELETE',
        registro_id=instance.id,
        descricao=descricao
    )
