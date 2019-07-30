from django import forms
from .models import *
class myDateForm(forms.Form):
    dataInicial = forms.CharField(max_length=100)
    dataFinal = forms.CharField(max_length=100)

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ("descricao","quantidade",)