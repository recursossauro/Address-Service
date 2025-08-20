from django import forms

class PostalForm(forms.Form):
    mensagem = forms.CharField(widget=forms.Textarea, required=True)
    destinatario = forms.CharField(max_length=100, required=True)
    imagem = forms.ImageField(required=False)