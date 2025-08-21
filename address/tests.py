# address/tests.py
from django.test import TestCase
from address.models import EnderecoBrasileiro, EstadoBrasileiro, Address


class EnderecoBrasileiroTestCase(TestCase):
    def setUp(self):
        # Dados de exemplo para o teste
        self.address_data = {
            "postal_system": "BR",
            "country": "BR",
            "logradouro":"Rua das Flores, 123",
            "estado":EstadoBrasileiro.objects.get(sigla = 'SP'),
            "cidade":"São Paulo",
            "numero":234,
            "complemento":"apartamento",
            "cep":"01234-567",
            "bairro": "Centro",
            "country": "BR",
        }

        # Cria o endereço usando a Factory
        address = EnderecoBrasileiro(**self.address_data)

        # Salva no banco de dados
        address.save()

    def test_create_brazilian_address(self):
        # Cria o endereço usando a Factory
        address = EnderecoBrasileiro(**self.address_data)

        # Salva no banco de dados
        address.save()

        # Verifica se o objeto foi criado corretamente
        self.assertEqual(address.logradouro, self.address_data["logradouro"])
        self.assertEqual(address.cep, self.address_data["cep"])
        self.assertIsInstance(address, EnderecoBrasileiro)  # Verifica o tipo

    def test_address_persistence(self):
        # Cria e salva o endereço
        address = EnderecoBrasileiro(**self.address_data)
        address.save()

        # Recupera o endereço do banco de dados
        saved_address = EnderecoBrasileiro.objects.get(id=address.id)

        # Verifica se os dados persistiram corretamente
        self.assertEqual(saved_address.logradouro, "Rua das Flores, 123")
        self.assertEqual(saved_address.cep, "01234-567")

    def test_invalid_postal_code(self):
        pass