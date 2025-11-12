from django.test import TestCase
from django.contrib.auth.models import User
from .models import Estoque, Maquina, Auditoria
from django.utils import timezone

class EstoqueMaquinaTestCase(TestCase):
    def setUp(self):
        # Criando um usuário para a auditoria
        self.user = User.objects.create_user(username="testeuser", password="senha123")

        # Criando itens de estoque
        self.peca1 = Estoque.objects.create(
            codigo="P001",
            nome="Motor Elétrico",
            descricao="Motor 220V de alta eficiência",
            quantidade=20,
            marca="WEG",
            fornecedor="Fornecedor A",
            preco=450.00,
            qtd_min=5,
            qtd_max=50
        )

        self.peca2 = Estoque.objects.create(
            codigo="P002",
            nome="Correia Industrial",
            descricao="Correia de borracha reforçada",
            quantidade=10,
            marca="BeltFlex",
            fornecedor="Fornecedor B",
            preco=80.00,
            qtd_min=2,
            qtd_max=30
        )

        # Criando uma máquina
        self.maquina = Maquina.objects.create(
            codigo="M001",
            nome="Torno Mecânico",
            descricao="Torno de precisão para corte de metal",
            localizacao="Setor 2",
            data_aquisicao="2022-03-15",
            status="Ativa",
        )
        self.maquina.pecas.set([self.peca1, self.peca2])

    def test_cadastro_estoque(self):
        """Verifica se o cadastro de peças no estoque é realizado corretamente."""
        self.assertEqual(self.peca1.nome, "Motor Elétrico")
        self.assertTrue(self.peca1.quantidade >= self.peca1.qtd_min)
        print("✔️ Teste 1 - Cadastro de peça de estoque concluído com sucesso.")

    def test_relacao_maquina_pecas(self):
        """Verifica se a máquina está corretamente associada às peças do estoque."""
        self.assertEqual(self.maquina.pecas.count(), 2)
        self.assertIn(self.peca1, self.maquina.pecas.all())
        print("✔️ Teste 2 - Relação máquina–peças validada com sucesso.")

    def test_limite_quantidade_estoque(self):
        """Verifica se a quantidade do item de estoque está dentro dos limites definidos."""
        dentro_limite = self.peca1.qtd_min <= self.peca1.quantidade <= self.peca1.qtd_max
        self.assertTrue(dentro_limite)
        print("✔️ Teste 3 - Validação de limites de estoque concluída com sucesso.")

    def test_status_maquina(self):
        """Verifica se o status inicial da máquina é 'Ativa'."""
        self.assertEqual(self.maquina.status, "Ativa")
        print("✔️ Teste 4 - Status da máquina validado com sucesso.")

    def test_registro_auditoria(self):
        """Verifica se um registro de auditoria pode ser criado corretamente."""
        log = Auditoria.objects.create(
            usuario=self.user,
            tabela="Estoque",
            acao="INSERT",
            registro_id=self.peca1.id,
            data_hora=timezone.now(),
            descricao="Peça cadastrada no estoque."
        )
        self.assertEqual(log.acao, "INSERT")
        self.assertEqual(log.usuario.username, "testeuser")
        print("✔️ Teste 5 - Registro de auditoria criado com sucesso.")
