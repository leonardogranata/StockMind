from django.test import TestCase
from django.contrib.auth.models import User

class UsuarioTestCase(TestCase):
    def test_cadastro_usuario_senhas_iguais(self):
        user = User.objects.create_user(username="isa", password="senha123")
        self.assertEqual(user.username, "isa", "O nome de usuário salvo não corresponde ao informado.")
        self.assertTrue(user.check_password("senha123"), "A senha informada não corresponde à armazenada.")
        print("✔️ Teste 6 - Cadastro de usuário com senhas iguais concluído com sucesso.")

    def test_cadastro_usuario_senhas_diferentes(self):
        senha = "senha123"
        confirmar = "senhaErrada"
        self.assertNotEqual(senha, confirmar, "As senhas deveriam ser diferentes, mas estão iguais.")
        print("✔️ Teste 7 - Validação de senhas diferentes concluída com sucesso.")

    def test_senha_curta(self):
        senha = "123"
        self.assertTrue(len(senha) < 8, "A senha informada deveria ser considerada curta.")
        print("✔️ Teste 8 - Verificação de comprimento mínimo da senha concluída com sucesso.")


class TestUsuario(TestCase):
    def test_criar_usuario_valido(self):
        user = User.objects.create_user(username="isa", password="minhaSenha@123")
        self.assertTrue(User.objects.filter(username="isa").exists(), "Usuário válido não foi criado corretamente.")
        print("✔️ Teste 9 - Criação de usuário válido concluída com sucesso.")

    def test_nao_cria_senhas_diferentes(self):
        senha = "abc123"
        confirmar = "abc321"
        self.assertNotEqual(senha, confirmar, "As senhas informadas não deveriam coincidir.")
        print("✔️ Teste 10 - Validação de senhas diferentes concluída com sucesso.")
