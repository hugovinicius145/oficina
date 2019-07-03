from django import forms
from .models import *

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["descricao","quantidade","valor_compra","valor_venda","categoria","codigo_fabrica"]

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ["descricao", "cnpj", "observacao"]

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ["logradouro","numero","bairro","cidade","estado","complemento"]

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome","cpf","status"]

class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ["telefone"]

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ["descricao","valor"]

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ["tipo","cliente"]

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ["servico","produto","quantidade","preco","item_cancelado"]