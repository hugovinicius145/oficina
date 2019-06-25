from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from pyrebase import pyrebase
from .models import *
from django.core.paginator import Paginator
from .forms import *
from datetime import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    lista_produtos = Produto.objects.order_by('id')
    data = {
        'lista_produtos' : lista_produtos,
    }
    return render(request, "oficina/index.html",data)


def produtos(request):
    lista_produtos = Produto.objects.all()
    paginator = Paginator(lista_produtos,30)
    page = request.GET.get('page')
    produtos = paginator.get_page(page)
    data = {        
        'produtos': produtos,
    }
    return render(request, "oficina/produtos.html",data)
def apagar_produto(request,id):
    produto = get_object_or_404(Produto,pk=id)
    produto.delete()
    return redirect('oficina:produtos')


def atualizar_produto(request, id):
    produto = get_object_or_404(Produto,pk=id)
    form = ProdutoForm(instance=produto)
    if(request.method == 'POST'):
        form = ProdutoForm(request.POST, instance=produto)
        if(form.is_valid()):
                produto = form.save(commit=False)
                produto.descricao = form.cleaned_data['descricao']
                produto.quantidade = form.cleaned_data['quantidade']
                produto.valor_compra = form.cleaned_data['valor_compra']
                produto.valor_venda = form.cleaned_data['valor_venda']
                produto.save()
                return redirect('oficina:produtos')
        else:
            return render(request, 'oficina/atualizarProduto.html', {'form': form, 'produto' : produto})
    elif(request.method == 'GET'):
        return render(request, 'oficina/atualizarProduto.html', {'form': form, 'produto' : produto})

def novo_produto(request):
    form = ProdutoForm()
    if(request.method == 'produto'):
        form = ProdutoForm(request.produto)
        if(form.is_valid()):
            produto_descricao = form.cleaned_data['descricao']
            produto_quantidade = form.cleaned_data['quantidade']
            produto_valor_compra = form.cleaned_data['valor_compra']
            produto_valor_venda = form.cleaned_data['valor_venda']
            produto_created = datetime.now()
            produto_modified = datetime.now()
            novo_produto = Produto(descricao=produto_descricao,quantidade=produto_quantidade,valor_compra=produto_valor_compra,
            valor_venda= produto_valor_venda,created= produto_created,modified=produto_modified)
            
            try:
                novo_produto.save()   
                msg = "Produto Cadastrado com Sucesso !!!"   
                tipo = "alert alert-success"             
            except:
                msg = "Erro ao Cadastar !!!"
                tipo = "alert alert-danger"
            aux_form = ProdutoForm()
            data ={
                'form': aux_form,
                'alerta': True,
                'msg': msg,
                'tipo_alerta' : tipo
            }
            #return redirect('oficina:novo_produto',data=True)
            return render(request, 'oficina/novoProduto.html',data)
    elif(request.method == 'GET'):
        return render(request, 'oficina/novoProduto.html', {'form': form})

def fornecedores(request):
    fornecedores = Fornecedor.objects.all()

    data = {
        "fornecedores": fornecedores
    }
    return render(request, "oficina/fornecedores.html",data)
