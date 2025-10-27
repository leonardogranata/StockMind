from django.contrib import admin
from .models import Estoque, Auditoria, Maquina

admin.site.register(Estoque)
admin.site.register(Auditoria)
admin.site.register(Maquina)
