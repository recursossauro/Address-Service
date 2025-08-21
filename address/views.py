from django.core.exceptions import ValidationError
from .forms import PostalSystemForm, EnderecoBrasileiroForm, USAddressForm
from django.shortcuts import render, redirect
from .models import Address, EnderecoBrasileiro, USAddress

from django.http import JsonResponse

def home(request):
    postalSystem_form = PostalSystemForm()
    address_form = None
    addresses    = None

    if request.method == 'POST':
        if 'postal_system_choice' in request.POST:
            postalSystem_form = PostalSystemForm(request.POST)
            if postalSystem_form.is_valid():
                postal_system = postalSystem_form.cleaned_data['postal_system_choice']
                if postal_system == 'BR':
                    address_form = EnderecoBrasileiroForm(initial={'postal_system': postal_system})
                    addresses = EnderecoBrasileiro.objects.all()
                elif postal_system == 'US':
                    address_form = USAddressForm()
                    addresses = USAddress.objects.all()

        elif 'postal_system' in request.POST:  # Formulário de endereço submetido
            postal_system = request.POST.get('postal_system')
            if postal_system == 'BR':
                address_form = EnderecoBrasileiroForm(request.POST)
                addresses = EnderecoBrasileiro.objects.all()
                if address_form.is_valid():
                    try:
                        address = Address.create_address(**address_form.cleaned_data)
                        address.save()
                        context = {"success": True, "address": str(address)}

                        return render(request, 'address/success.html', context)
                    except ValidationError as e:
                        return JsonResponse({"error": str(e)}, status=400)


    return render(request, 'address/home.html', {
        'country_form': postalSystem_form,
        'address_form': address_form,
        'addresses':    addresses
    })

