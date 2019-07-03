from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from .forms import *
from datetime import datetime
from django.contrib.auth.decorators import login_required

################ Produtos ###################
def index(request):
    lista_produtos = Produto.objects.order_by('id')
    data = {
        'lista_produtos' : lista_produtos,
    }
    return render(request, "oficina/index.html",data)


def produtos(request):
    lista_produtos = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        lista_produtos = Produto.objects.filter(descricao__icontains=search)
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
                form.save()
                return redirect('oficina:produtos')
        else:
            return render(request, 'oficina/atualizarProduto.html', {'form': form, 'produto' : produto})
    elif(request.method == 'GET'):
        return render(request, 'oficina/atualizarProduto.html', {'form': form, 'produto' : produto})

def novo_produto(request):
    form = ProdutoForm()
    if(request.method == 'POST'):
        form = ProdutoForm(request.POST)
        if(form.is_valid()):                       
            try:
                form.save()   
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
            return render(request, 'oficina/novoProduto.html',data)        
    elif(request.method == 'GET'):
        return render(request, 'oficina/novoProduto.html', {'form': form})
############ Fornecedores ################
def fornecedores(request):
    fornecedores = Fornecedor.objects.all()    
    data = {
        'fornecedores': fornecedores,
    }
    return render(request, "oficina/fornecedores.html",data)

def novo_fornecedor(request):
    form = FornecedorForm()
    form_endereco = EnderecoForm()
    form_telefone = TelefoneForm()
    data = {'form': form, 'form_endereco': form_endereco,'form_telefone':form_telefone}
    if (request.method == 'POST'):
        form = FornecedorForm(request.POST)
        form_endereco = EnderecoForm(request.POST)
        form_telefone = TelefoneForm(request.POST)
        if form.is_valid() and form_endereco.is_valid() and form_telefone.is_valid():                                                                                                
            try:
                form_endereco.save()
                form.instance.endereco = form_endereco.instance
                        
                #form.save()
                form_telefone.save()
                form.instance.telefone = form_telefone.instance
                form.save()
                #form_telefone.instance.fornecedor = form.instance
                # form_telefone.save()
                ###### Variaveis para mostrar na tela se foi cadastrado ou deu erro #######
                msg = "Fornecedor Cadastrado com Sucesso !!!"   
                tipo = "alert alert-success"
            except:
                msg = "Erro ao Cadastar !!!"
                tipo = "alert alert-danger"
            data = {
                'form': FornecedorForm(), 
                'form_endereco': EnderecoForm(),
                'form_telefone': TelefoneForm(),
                'alerta': True,
                'msg': msg,
                'tipo_alerta' : tipo
                }
            return render(request,'oficina/novoFornecedor.html',data)
    return render(request,'oficina/novoFornecedor.html',data)

def atualizar_fornecedor(request,id):
    fornecedor = get_object_or_404(Fornecedor,pk=id)    
    form = FornecedorForm(instance=fornecedor)

    endereco = get_object_or_404(Endereco,pk=fornecedor.get_endereco())
    form_endereco = EnderecoForm(instance=endereco)

    telefone = get_object_or_404(Telefone,pk=fornecedor.get_telefone())
    form_telefone = TelefoneForm(instance=telefone)
    data = {'form':form, 'form_endereco':form_endereco,'form_telefone':form_telefone}
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance = fornecedor)
        form_endereco = EnderecoForm(request.POST,instance=endereco)
        form_telefone = TelefoneForm(request.POST,instance=telefone)
        if form.is_valid() and form_endereco.is_valid() and form_telefone.is_valid():
            form_endereco.save()
            form.instance.endereco = form_endereco.instance
            form_telefone.save()
            form.instance.telefone = form_telefone.instance
            form.save()
            return redirect('oficina:fornecedores')
            
    elif request.method == 'GET':
        return render(request,'oficina/atualizarFornecedor.html',data)
def apagar_fornecedor(request,id):
    fornecedor = get_object_or_404(Fornecedor,pk=id)
    fornecedor.delete()
    return redirect('oficina:fornecedores')

################### Clientes ################################
def clientes(request):
    lista_clientes = Cliente.objects.all()
    paginator = Paginator(lista_clientes,30)
    page = request.GET.get('page')
    clientes = paginator.get_page(page)
    data = {        
        'clientes': clientes,
    }
    return render(request, "oficina/clientes.html",data)

def apagar_cliente(request,id):
    cliente = get_object_or_404(Cliente,pk=id)
    cliente.delete()
    return redirect('oficina:clientes')

def novo_cliente(request):
    form_cliente = ClienteForm()
    form_endereco = EnderecoForm()
    form_telefone = TelefoneForm()
    data = {'form_cliente':form_cliente, 'form_endereco':form_endereco, 'form_telefone':form_telefone}

    if (request.method == 'POST'):
        form_cliente = ClienteForm(request.POST)
        form_endereco = EnderecoForm(request.POST)
        form_telefone = TelefoneForm(request.POST)

        if form_cliente.is_valid() and form_endereco.is_valid() and form_telefone.is_valid():
            try:
                form_endereco.save()
                form_cliente.instance.endereco = form_endereco.instance

                form_telefone.save()
                form_cliente.instance.telefone = form_telefone.instance

                form_cliente.save()
                ###### Variaveis para mostrar na tela se foi cadastrado ou deu erro #######
                msg = "Cliente Cadastrado com Sucesso !!!"   
                tipo = "alert alert-success"
            except:
                msg = "Erro ao Cadastar !!!"
                tipo = "alert alert-danger"

            data = {
                'form_cliente':ClienteForm(), 
                'form_endereco':EnderecoForm(), 
                'form_telefone':TelefoneForm(),
                'alerta': True,
                'msg': msg,
                'tipo_alerta' : tipo
                }
            return render(request,'oficina/novoCliente.html',data) 
    elif request.method == 'GET':
        return render(request,'oficina/novoCliente.html',data)

def atualizar_cliente(request,id):
    cliente = get_object_or_404(Cliente,pk=id)
    form_cliente = ClienteForm(instance=cliente)

    endereco = get_object_or_404(Endereco,pk=cliente.get_endereco())
    form_endereco = EnderecoForm(instance=endereco)

    telefone = get_object_or_404(Telefone,pk=cliente.get_telefone())
    form_telefone = TelefoneForm(instance=telefone)

    data ={'form_cliente':form_cliente,'form_endereco':form_endereco,'form_telefone':form_telefone}
    if(request.method == 'POST'):
        form_cliente = ClienteForm(request.POST, instance=cliente)
        form_endereco = EnderecoForm(request.POST,instance=endereco)
        form_telefone = TelefoneForm(request.POST,instance=telefone)
        if(form_cliente.is_valid() and form_endereco.is_valid() and form_telefone.is_valid()):                
           
            form_endereco.save()
            form_cliente.instance.endereco = form_endereco.instance

            form_telefone.save()
            form_cliente.instance.telefone = form_telefone.instance

            form_cliente.save()
            return redirect('oficina:clientes')       
    elif(request.method == 'GET'):
        return render(request, 'oficina/atualizarCliente.html', data)

####################### Servicos ######################

def servicos(request):
    lista_servicos = Servico.objects.all()
    paginator = Paginator(lista_servicos,30)
    page = request.GET.get('page')
    servicos = paginator.get_page(page)
    data = {        
        'servicos': servicos,
    }
    return render(request, "oficina/servicos.html",data)

def apagar_servico(request,id):
    servico = get_object_or_404(Servico,pk=id)
    servico.delete()
    return redirect('oficina:servicos')

def novo_servico(request):
    form  = ServicoForm()
    data = {'form':form}

    if (request.method == 'POST'):
        form = ServicoForm(request.POST)
        if (form.is_valid()):
            try:
                form.save()
                msg = "Servico Cadastrado com Sucesso !!!"   
                tipo = "alert alert-success"
            except:
                msg = "Erro ao Cadastar !!!"
                tipo = "alert alert-danger"

            data = {
                'form':ServicoForm(),
                'alerta': True,
                'msg': msg,
                'tipo_alerta' : tipo
                }
            return render(request,'oficina/novoServico.html',data) 
    elif (request.method == 'GET'):
        return render(request,'oficina/novoServico.html',data)
def atualizar_servico(request,id):
    servico = get_object_or_404(Servico,pk=id)
    form  = ServicoForm(instance=servico)
    data = {'form':form}

    if (request.method == 'POST'):
        form = ServicoForm(request.POST,instance=servico)
        if (form.is_valid()):
            try:
                form.save()
                msg = "Servico Alterado com Sucesso !!!"   
                tipo = "alert alert-success"
            except:
                msg = "Erro ao Cadastar !!!"
                tipo = "alert alert-danger"

            data = {
                'form':form,
                'alerta': True,
                'msg': msg,
                'tipo_alerta' : tipo
                }
            return render(request,'oficina/atualizarServico.html',data) 
    elif (request.method == 'GET'):
        return render(request,'oficina/novoServico.html',data)

################### Vendas ########################
def nova_venda(request):
    form_venda = VendaForm()
    form_item_venda = ItemVendaForm()

    data = {'form_venda':form_venda,'form_item_venda':form_item_venda}
    
    if (request.method == 'POST'):
        form_venda = VendaForm(request.POST)
        if (form_venda.is_valid()):
            try:
                form_venda.instance.vendedor = request.user
                form_venda.save()
                msg = "venda Realizada Com Sucesso !!!"   
                tipo = "alert alert-success"
            except:
                msg = "Erro ao Cadastar !!!"
                tipo = "alert alert-danger"

            data = {
                'form_venda':VendaForm(),
                'alerta': True,
                'msg': msg,
                'tipo_alerta' : tipo,
                }
    elif(request.method == 'GET'):
        return render(request,'oficina/novaVenda.html',data)