from django import forms
from .models import Address, GenericAddress, EnderecoBrasileiro, USAddress

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['postal_system', 'country']

        widgets = {
            'postal_system': forms.HiddenInput(),
        }

class EnderecoBrasileiroForm(forms.ModelForm):
    class Meta:
        model = EnderecoBrasileiro
        fields = ['postal_system', 'country', 'logradouro', 'numero', 'complemento', 'cidade', 'estado', 'cep', 'bairro']

        widgets = {
            'postal_system': forms.HiddenInput(),
        }

class USAddressForm(forms.ModelForm):
    class Meta:
        model = USAddress
        fields = ['postal_system', 'country', 'street', 'city', 'state', 'zip_code']

        widgets = {
            'postal_system': forms.HiddenInput(),
        }

# Formulário inicial para seleção de país
class PostalSystemForm(forms.Form):
    postal_system_choices = Address.getSubclasses()
    postal_system_choice = forms.ChoiceField(choices=postal_system_choices, label="Postal System")