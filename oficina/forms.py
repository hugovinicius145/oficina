from django import forms
from .models import *

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["descricao","quantidade","valor_compra","valor_venda"]

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ["descricao", "cnpj", "observacao"]

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ["logradouro","numero","bairro","cidade","estado","complemento"]