from django import forms
from django.forms import modelform_factory

from .models import (
    Address,
    EnderecoBrasileiro, EstadoBrasileiro,
    GenericAddress)

from .forms import EnderecoBrasileiroForm

class AddressTools:

    postal_system_code = None
    model = None
    address_form = None
    address_fields_html = 'address_fields_html'
    address_html        = 'address_html'

    _subclasses = {}  # Dictionary of postal system to Address Model class: {'BR': BrazilianAddress, ...}

    def __init_subclass__(cls, postal_system_code=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if postal_system_code:
            cls.postal_system_code = postal_system_code
            AddressTools._subclasses[postal_system_code] = cls

            # Cria um FormModel para a classe
            if cls.model and not cls.address_form:
                cls._create_address_form()

    class Meta:
        abstract = True

    @classmethod
    def getSubclasses(cls):
        subclasses = None
        if cls._subclasses:
            subclasses = [(code, sub_class.postal_system_name) for (code, sub_class) in cls._subclasses.items()]

        return subclasses

    @classmethod
    def AddressToolsFactory(cls, **kwargs):
        addressTool = None
        if 'postal_system_code' in kwargs:
            subclass = cls._subclasses.get(kwargs.get('postal_system_code'))
            if not subclass:
                raise ValueError(f"Postal system not soported: {kwargs.get('postal_system_code')}")
            addressTool = subclass()
        else:
            raise ValueError(f"The postal_system_code is required.")

        return addressTool

    @classmethod
    def get_address_all(cls):
        addresses_tool = []
        for (id, cl) in cls._subclasses.items():
            addresses_tool.append({id: cl.objects.all()})

        return addresses_tool

    @classmethod
    def getAddressHTML(cls):
        return cls.address_html

    @classmethod
    def getAddressFieldsHTML(cls):
        return cls.address_fields_html

    @classmethod
    def _create_address_form(cls):
        """Cria o ModelForm dinamicamente após a classe estar totalmente definida"""
        cls.address_form = modelform_factory(
            cls.model,
            fields='__all__',
            widgets={
                'postal_system': forms.HiddenInput(),
            }
        )

    @classmethod
    def getAddressFromRequest(cls, request):
        if request.method == 'POST':
            form = cls.address_form(request.POST)

            if form.is_valid():
                return form.save(commit=False)
            else:
                print("❌ Erros:", form.errors)

                instance = cls.model()

                # Preenche campos normais
                for field_name in ['cep', 'cidade', 'bairro', 'logradouro', 'complemento', 'country']:
                    if field_name in request.POST:
                        setattr(instance, field_name, request.POST[field_name])

                # Campos especiais
                if 'numero' in request.POST and request.POST['numero']:
                    try:
                        instance.numero = int(request.POST['numero'])
                    except ValueError:
                        print("⚠️  Número inválido")

                # Processamento do estado (ForeignKey)
                if 'estado' in request.POST and request.POST['estado']:
                    try:
                        estado_id = int(request.POST['estado'])
                        instance.estado = EstadoBrasileiro.objects.get(pk=estado_id)
                    except (ValueError, EstadoBrasileiro.DoesNotExist):
                        print("⚠️  Estado inválido ou não encontrado")

                return instance

    @classmethod
    def save(cls, *args, **kwargs):
        cls.model(*args, **kwargs).save()


class EnderecoBrasileiroTools(AddressTools, postal_system_code=EnderecoBrasileiro.postal_system_code):

    address_fields_html = 'address/cad_endereco_brasileiro.html'
    address_html        = 'address/endereco_brasileiro.html'
    model = EnderecoBrasileiro
    clsEstado = EstadoBrasileiro

    @classmethod
    def estados(cls):
        return EstadoBrasileiro.objects.all()

    @classmethod
    def getEstado(cls, pk):
        return cls.clsEstado.objects.get(pk=pk)
