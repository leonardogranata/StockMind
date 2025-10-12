from django.core.management.base import BaseCommand
import pandas as pd
from estoque.models import Estoque
from analise.models import Consumo
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = "Popula a tabela Consumo a partir de um CSV"

    def handle(self, *args, **options):
        df = pd.read_csv('dados_teste.csv')  # caminho do CSV
        usuario = User.objects.first()  # ou outro usuário que queira associar

        for _, row in df.iterrows():
            try:
                item = Estoque.objects.get(nome__iexact=row['item'])
            except Estoque.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Item {row['item']} não encontrado no estoque."))
                continue

            # cria ou atualiza consumo existente no mesmo dia
            data = pd.to_datetime(row['data']).date()
            consumo_existente = Consumo.objects.filter(item=item, data=data).first()
            if consumo_existente:
                consumo_existente.quantidade += int(row['quantidade'])
                consumo_existente.save()
            else:
                Consumo.objects.create(
                    item=item,
                    quantidade=int(row['quantidade']),
                    data=data,
                    usuario=usuario
                )

        self.stdout.write(self.style.SUCCESS('Consumos populados com sucesso!'))
