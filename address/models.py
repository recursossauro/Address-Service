# models.py
from django.db import models
from django.db.models import CharField


class Address(models.Model):
    postal_system_code = None
    postal_system_name = None
    __subclasses = {} # Dictionary of postal system to Address Model class: {'BR': BrazilianAddress, ...}

    def __init_subclass__(cls, postal_system_code=None, **kwargs):
        super.__init_subclass__(**kwargs)
        if postal_system_code:
            Address.__subclasses[postal_system_code]=cls
            cls.postal_system_code = postal_system_code

    postal_system = models.CharField(max_length=5, default='00000')  # Ex: 'BR', 'US_01', 'US_02'
    country = models.CharField('Country', max_length=2, default='BR')  # Ex: 'BR', 'US'

    class Meta:
        abstract = True

    @classmethod
    def getSubclasses(cls):
        subclasses = None
        if cls.__subclasses:
            subclasses = [(code, sub_class.postal_system_name) for (code, sub_class) in cls.__subclasses.items()]

        return subclasses

    @classmethod
    def create_address(cls, **kwargs):
        address = None
        if 'postal_system' in kwargs:
            subclass = cls.__subclasses.get(kwargs.get('postal_system'))
            if not subclass:
                raise ValueError(f"Postal system not soported: {kwargs.get('postal_system')}")
            address = subclass(**kwargs)
        else:
            raise ValueError(f"The postal_system is required.")

        return address

    @classmethod
    def get_address_all(cls):
        addresses = []
        for (id, cl) in cls.__subclasses.items():
            addresses.append({id:cl.objects.all()})

        return addresses

    def save(self, *args, **kwargs):
        if hasattr(self, 'postal_system_code'):
            self.postal_system = self.postal_system_code
        super().save(*args, **kwargs)


# Generic Address
class GenericAddress(Address, postal_system_code='99'):
    postal_system_name = "Generic Postal System"
    address = models.TextField("Address", max_length=2000)

    def __str__(self):
        return f"{self.address}"
# Brazilian Address

# Estados Brasileiros
class EstadoBrasileiro(models.Model): #Estado ou Distrito
    sigla = models.CharField("Sigla", max_length=2)
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return f"{self.sigla} - {self.name}"

class EnderecoBrasileiro(Address, postal_system_code='BR'):

    postal_system_name = "Sistema Brasileiro de Endereços"

    country      = models.CharField('País', max_length=2, default='BR')  # Ex: 'BR', 'US'
    logradouro   = models.CharField('Logradouro', max_length=255)
    estado       = models.ForeignKey(EstadoBrasileiro, verbose_name="Estado ou Distrito", on_delete=models.PROTECT, null=True, blank=True)  # Estado ou Distrito
    cidade       = models.CharField("Cidade", max_length=100)
    numero       = models.SmallIntegerField(verbose_name='Número', null=True, blank=True)  # Número da casa, apartamento, etc
    complemento  = models.CharField(verbose_name='Complemento', max_length=255, null=True, blank='True')  # Casa, Apartamento, etc
    cep          = models.CharField(verbose_name='CEP', max_length=9)  # CEP (XXXXX-XXX)
    bairro       = models.CharField(verbose_name='Bairro', max_length=100)  # Bairro

    def __str__(self):
        return f"{self.logradouro}, {self.complemento}, {self.numero}, {self.bairro}, {self.cidade}/{self.estado} - CEP: {self.cep}"

    @classmethod
    def getSigla(cls, cd_estado):
        return EstadoBrasileiro.objects.get(id=cd_estado)

    @classmethod
    def test(cls):

        # Teste Cria e exclui Endereço Brasileiro
        # Dados de exemplo para o teste
        address_data = {
            "postal_system_code": "BR",
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
        address = Address.create_address(**address_data)

        # Salva no banco de dados
        address.save()

        # Recupera o endereço do banco de dados
        saved_address = EnderecoBrasileiro.objects.get(id=address.id)

        print(saved_address.postal_system_code, saved_address.postal_system, saved_address)

        address.delete()

# USA Address
class USAddress(Address, postal_system_code='US'):
    postal_system_name = "USA Postal System"

    country = models.CharField( max_length=2, default='US')  # Ex: 'BR', 'US'
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)  # ZIP+4 (XXXXX-XXXX)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"
