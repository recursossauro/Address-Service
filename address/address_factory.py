from django import forms
from django.forms import modelform_factory
from functools import wraps
from typing import Dict, Any, Type
from .models import (
    EnderecoBrasileiro, EstadoBrasileiro,
    GenericAddress)


def auto_extract_fields(func):
    """Decorator que automaticamente extrai campos do request"""

    @wraps(func)
    def wrapper(cls, request):
        if not hasattr(cls, '_field_source'):
            cls._field_source = getattr(cls, 'address_form', None) or getattr(cls, 'model', None)

        data = {}
        fields = cls._get_fields_from_source(cls._field_source)

        for field_name, field in fields.items():
            if field_name in request.POST:
                data[field_name] = cls._convert_field_value(field, request.POST[field_name])

        return func(cls, request, data)

    return wrapper


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
    def _get_fields_from_source(cls, field_source) -> Dict[str, Any]:
        """Obtém campos do formulário ou modelo"""
        if field_source and issubclass(field_source, forms.BaseForm):
            return field_source.base_fields
        elif field_source and issubclass(field_source, models.Model):
            return {f.name: f for f in field_source._meta.get_fields()
                    if isinstance(f, models.Field)}
        else:
            raise TypeError("Fonte de campos deve ser Form ou Model")

    @classmethod
    def _convert_field_value(cls, field, raw_value: str) -> Any:
        """Converte valor baseado no tipo do campo"""
        # Para formulários Django
        if isinstance(field, forms.Field):
            try:
                return field.clean(raw_value)
            except forms.ValidationError:
                return raw_value  # Fallback para validação falha

        # Para modelos Django
        elif isinstance(field, models.Field):
            if isinstance(field, (models.IntegerField, models.AutoField)):
                return int(raw_value) if raw_value and raw_value.isdigit() else None
            elif isinstance(field, models.BooleanField):
                return raw_value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(field, models.DateField):
                # Implementar parsing de data conforme necessário
                return raw_value
            else:
                return raw_value  # Strings e campos simples

        return raw_value  # Fallback


    @classmethod
    @auto_extract_fields
    def getAddressFromRequest(cls, request, extracted_data=None):
        """Método agora recebe dados extraídos automaticamente"""
        return extracted_data or {}

    @classmethod
    def save(cls, *args, **kwargs):
        cls.model(*args, **kwargs).save()


class EnderecoBrasileiroTools(AddressTools, postal_system_code=EnderecoBrasileiro.postal_system_code):

    address_fields_html = 'address/cad_endereco_brasileiro.html'
    address_html        = 'address/endereco_brasileiro.html'
    model = EnderecoBrasileiro
    clsEstado = EstadoBrasileiro

    @classmethod
    def getAddressFromRequest(cls, request):
        """Pode ser sobrescrito para comportamentos específicos"""
        data = super().getAddressFromRequest(request)

        # Validações específicas do Brasil
        if 'cep' in data:
            data['cep'] = cls._formatar_cep(data['cep'])

        return data

    @staticmethod
    def _formatar_cep(cep: str) -> str:
        """Formata CEP no padrão brasileiro"""
        cep = ''.join(filter(str.isdigit, cep))
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep

    @classmethod
    def estados(cls):
        return EstadoBrasileiro.objects.all()

    @classmethod
    def getEstado(cls, pk):
        return cls.clsEstado.objects.get(pk=pk)
