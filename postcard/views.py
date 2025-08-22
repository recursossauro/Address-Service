from django.shortcuts import render
from address.address_factory import AddressTools

addressTools = AddressTools.AddressToolsFactory(**{'postal_system_code': 'BR'})

def enviar_postal(request):

    context = {'addressTools':addressTools}

    return render(request, 'postcard/enviar_postal.html', context)

def visualizar_postal(request):
    if request.method == 'POST':

        # Captura os dados do formulário
        imagem       = request.FILES.get('imagem')
        imagem_url   = imagem.url if imagem else '/static/postcard/post_image.png'
        destinatario = request.POST.get('destinatario', '')
        address      = addressTools.getAddressFromRequest(request)

        # print(f'\n\n\n\n\n {type(address).__name__} {address} \n\n\n\n\n\n\n')


        context = {
            'mensagem': request.POST.get('mensagem',''),
            'imagem_url':   imagem_url,
            'addressTools': addressTools,
            'destinatario': destinatario,
            'address': address,
        }

        return render(request, 'postcard/visualizar_postal.html', context)

    return render(request, 'postcard/enviar_postal.html')
