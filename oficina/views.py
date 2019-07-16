from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from .models import *
from django.core.paginator import Paginator
from .forms import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.template import RequestContext
from django.forms import inlineformset_factory, modelformset_factory, formset_factory
from urllib.parse import urlencode
################ Produtos ###################
def index(request):
    '''lista_produtos = Produto.objects.order_by('id')
    data = {
        'lista_produtos' : lista_produtos,
    }
    return render(request, "oficina/index.html",data)'''
    return redirect('oficina:orcamentos')


def produtos(request,order=None):
    lista_produtos = Produto.objects.all().order_by('descricao')
    search = request.GET.get('search')
    if search:
        if search.isdigit():        
            lista_produtos = Produto.objects.filter(id=search)
        else:
            lista_produtos = Produto.objects.filter(descricao__icontains=search)
    
    
    '''paginator = Paginator(lista_produtos,4)
    page = request.GET.get('page')
    produtos = paginator.get_page(page)'''
    data = {        
        'produtos': lista_produtos,
    }
    return render(request, "oficina/produtos/produtos.html",data)
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
            return render(request, 'oficina/produtos/atualizarProduto.html', {'form': form, 'produto' : produto})
    elif(request.method == 'GET'):
        return render(request, 'oficina/produtos/atualizarProduto.html', {'form': form, 'produto' : produto})

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
            return render(request, 'oficina/produtos/novoProduto.html',data)                    
    elif(request.method == 'GET'):
        return render(request, 'oficina/produtos/novoProduto.html', {'form': form})


def validar_descricao_produto(request):
    descricao = request.GET.get('descricao', None)
    data = {
        'is_taken': Produto.objects.filter(descricao__iexact=descricao).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Existe um Produto Cadastrado com essa Descrição.'
    return JsonResponse(data)
############ Fornecedores ################
def fornecedores(request):
    fornecedores = Fornecedor.objects.all().order_by('descricao')    
    data = {
        'fornecedores': fornecedores,
    }
    return render(request, "oficina/fornecedores/fornecedores.html",data)

def novo_fornecedor(request):
    form = FornecedorForm()
    form_endereco = EnderecoForm()
    form_telefone = TelefoneForm()

    base_url = '/fornecedores/new'
    msg_sucesso = request.GET.get('msg_sucesso')
    msg_erro = request.GET.get('msg_erro')    
    data = {
        'form': form, 
        'form_endereco': form_endereco,
        'form_telefone':form_telefone,
        'msg_sucesso':msg_sucesso,
        'msg_erro':msg_erro,        
        }
    if (request.method == 'POST'):
        form = FornecedorForm(request.POST)
        form_endereco = EnderecoForm(request.POST)
        form_telefone = TelefoneForm(request.POST)
        if form.is_valid() and form_endereco.is_valid() and form_telefone.is_valid():                                                                                                
            try:
                form_endereco.save()
                form.instance.endereco = form_endereco.instance
                                        
                form_telefone.save()
                form.instance.telefone = form_telefone.instance

                form.save() 
                ###### Variaveis para mostrar na tela se foi cadastrado ou deu erro #######
                msg_sucesso = "Fornecedor Cadastrado com Sucesso !!!" 
                query_string = urlencode({'msg_sucesso': msg_sucesso})                 
            except:
                msg_erro = "Erro ao Cadastar !!!" 
                query_string = urlencode({'msg_erro': msg_erro}) 

            url = '{}?{}'.format(base_url,query_string)                                                   
            return redirect(url)  
    return render(request,'oficina/fornecedores/novoFornecedor.html',data)

def atualizar_fornecedor(request,id):
    fornecedor = get_object_or_404(Fornecedor,pk=id)    
    form = FornecedorForm(instance=fornecedor)

    endereco = get_object_or_404(Endereco,pk=fornecedor.get_endereco())
    form_endereco = EnderecoForm(instance=endereco)

    telefone = get_object_or_404(Telefone,pk=fornecedor.get_telefone())
    form_telefone = TelefoneForm(instance=telefone)

    base_url = '/fornecedores/edit/{}'.format(fornecedor.id)
    msg_sucesso = request.GET.get('msg_sucesso')
    msg_erro = request.GET.get('msg_erro')  
    data = {
        'form':form,
        'form_endereco':form_endereco,
        'form_telefone':form_telefone,
        'fornecedor':fornecedor,
        'msg_sucesso':msg_sucesso,
        'msg_erro':msg_erro,
        }
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance = fornecedor)
        form_endereco = EnderecoForm(request.POST,instance=endereco)
        form_telefone = TelefoneForm(request.POST,instance=telefone)
        if form.is_valid() and form_endereco.is_valid() and form_telefone.is_valid():
            try:
                form_endereco.save()
                form.instance.endereco = form_endereco.instance
                form_telefone.save()
                form.instance.telefone = form_telefone.instance
                form.save()
                msg_sucesso = "Fornecedor Atualizado com Sucesso !!!" 
                query_string = urlencode({'msg_sucesso': msg_sucesso})
            except:
                msg_erro = "Erro ao Atualizar !!!" 
                query_string = urlencode({'msg_erro': msg_erro}) 

            url = '{}?{}'.format(base_url,query_string)
            return redirect(url)
            
    elif request.method == 'GET':
        return render(request,'oficina/fornecedores/atualizarFornecedor.html',data)
def apagar_fornecedor(request,id):
    fornecedor = get_object_or_404(Fornecedor,pk=id)
    fornecedor.delete()
    return redirect('oficina:fornecedores')

################### Clientes ################################
def clientes(request):
    lista_clientes = Cliente.objects.all().order_by('nome')
    search = request.GET.get('search')
    if search:
        if search.isdigit():        
            lista_clientes = Cliente.objects.filter(id=search)
        else:
            lista_clientes = Cliente.objects.filter(nome__icontains=search)
        
    paginator = Paginator(lista_clientes,30)
    page = request.GET.get('page')
    clientes = paginator.get_page(page)
    data = {        
        'clientes': clientes,
        'name':'Cliente',
        'url':'oficina:clientes',
    }
    return render(request, "oficina/clientes/clientes.html",data)

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
            return render(request,'oficina/clientes/novoCliente.html',data) 
    elif request.method == 'GET':
        return render(request,'oficina/clientes/novoCliente.html',data)

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
        return render(request, 'oficina/clientes/atualizarCliente.html', data)

####################### Servicos ######################

def servicos(request):
    lista_servicos = Servico.objects.all()
    paginator = Paginator(lista_servicos,30)
    page = request.GET.get('page')
    servicos = paginator.get_page(page)
    data = {        
        'servicos': servicos,
    }
    return render(request, "oficina/servicos/servicos.html",data)

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
            return render(request,'oficina/servicos/novoServico.html',data) 
    elif (request.method == 'GET'):
        return render(request,'oficina/servicos/novoServico.html',data)
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
            return render(request,'oficina/servicos/atualizarServico.html',data) 
    elif (request.method == 'GET'):
        return render(request,'oficina/servicos/novoServico.html',data)

################### Vendas ########################

def nova_venda(request):
    form_orcamento = OrcamentoVendaForm()
    form_orcamento.initial['vendedor'] = request.user        
    data = {'form_orcamento':form_orcamento,'vendedor':request.user}    
    if request.method == 'POST':
        form_orcamento = OrcamentoVendaForm(request.POST)    
        
        if form_orcamento.is_valid(): 
            form_orcamento.save()
            orcamento_id = form_orcamento.instance.id
            return redirect('oficina:novo_item',orcamento_id=orcamento_id)            
    elif request.method == 'GET':        
        return render(request,'oficina/vendas/novaVenda.html',data)

def finalizar_venda(request, orcamento_id):
    orcamento = get_object_or_404(OrcamentoVenda,pk=orcamento_id)
    orcamento.status = True
    venda = Venda(orcamento=orcamento)    

    ### Metodo para dar baixa no estoque
    base_url = '/vendas/add/item/{}'.format(orcamento_id)
    lista_itens = ItemVenda.objects.filter(orcamento=orcamento_id)
    for item in lista_itens:
        if item.produto_id != None:
            produtos = Produto.objects.filter(id=item.produto_id)
            for produto in produtos:
                if produto.baixar_estoque(item.quantidade):
                    produto.save()
                else:
                    msg_estoque_baixo = 'Quantidade de {} Excede o Estoque'.format(produto.descricao)
                    query_string = urlencode({'msg_estoque_baixo': msg_estoque_baixo})
                    url = '{}?{}'.format(base_url,query_string)                    
                    return redirect(url)
    try:
        
        orcamento.save()
        venda.save()
        return redirect('oficina:orcamentos')
    except:
        query_string = urlencode({'msg_erro_finalizar': 'Não Foi possivel Finalizar a Venda'})
        url = '{}?{}'.format(base_url,query_string)
        return redirect(url)

def novo_item(request, orcamento_id):
    orcamento = get_object_or_404(OrcamentoVenda,pk=orcamento_id)
    
    form = ItemVendaForm()
    lista_itens = ItemVenda.objects.filter(orcamento=orcamento_id).order_by('produto')

    ### Mensagens de erro
    msg_estoque_baixo = request.GET.get('msg_estoque_baixo')
    msg_erro_finalizar = request.GET.get('msg_erro_finalizar')

    data = {
        'form':form,
        'lista_itens':lista_itens,
        'orcamento_id':orcamento_id,
        'valor_total':orcamento.preco_total,
        'orcamento':orcamento,
        'servico' : 'Servico',
        'produto' : 'Produto',
        'msg_estoque_baixo':msg_estoque_baixo,
        'msg_erro_finalizar':msg_erro_finalizar,        
    }
    if request.method == 'POST':
        form = ItemVendaForm(request.POST)            
        if form.is_valid():
            form.instance.orcamento_id = orcamento_id
            form.save()                             
            return redirect('oficina:novo_item',orcamento_id=orcamento_id)
    elif request.method == 'GET':        
        return render(request,'oficina/vendas/novoItemVenda.html',data)

def atualizar_item(request, orcamento_id, id):
    item = get_object_or_404(ItemVenda,pk=id)
    form = ItemVendaForm(instance=item)
    lista_itens = ItemVenda.objects.filter(orcamento=orcamento_id)
    data = {'form':form,'lista_itens':lista_itens,'orcamento_id':orcamento_id}
    if request.method == 'POST':
        form = ItemVendaForm(request.POST,instance=item)            
        if form.is_valid():
            form.instance.orcamento_id = orcamento_id
            form.save()                             
            return redirect('oficina:novo_item',orcamento_id=orcamento_id)
    elif request.method == 'GET':        
        return render(request,'oficina/vendas/novoItemVenda.html',data)
            
def apagar_item(request,orcamento_id,id):
    item = get_object_or_404(ItemVenda,pk=id)
    item.delete()
    return redirect('/vendas/add/item/'+str(orcamento_id))

def vendas(request):
    '''lista_vendas = Venda.objects.all()
    search = request.GET.get('search')
    if search:
        if search.isdigit():        
            lista_vendas = Venda.objects.filter(id=search)
        else:
            lista_vendas = Venda.objects.filter(cliente__nome__icontains=search)
        
    paginator = Paginator(lista_vendas,30)
    page = request.GET.get('page')
    vendas = paginator.get_page(page)
    data = {        
        'vendas': vendas,
    }'''
    # return render(request, "oficina/vendas/vendas.html",data)
    return redirect('oficina:orcamentos')

def orcamentos(request):
    lista_orcamento = OrcamentoVenda.objects.all().order_by('-modified')
    search = request.GET.get('search')
    if search:
        if search.isdigit():        
            lista_orcamento = OrcamentoVenda.objects.filter(id=search)
        else:
            lista_orcamento = OrcamentoVenda.objects.filter(cliente__nome__icontains=search)
        
    paginator = Paginator(lista_orcamento,30)
    page = request.GET.get('page')
    orcamentos = paginator.get_page(page)    
    data = {        
        'orcamentos': orcamentos,    
    }
    return render(request, "oficina/vendas/orcamentoVendas.html",data)

def apagar_orcamento(request, id):
    orcamento = get_object_or_404(OrcamentoVenda,pk=id)
    orcamento.delete()
    return redirect('oficina:orcamentos')

def atualizar_orcamento(request,id):
    orcamento = get_object_or_404(OrcamentoVenda,pk=id)
    form_orcamento = OrcamentoVendaForm(instance=orcamento)
    # form_orcamento.initial['vendedor'] = request.user 
    data = {'form_orcamento':form_orcamento}    
    if request.method == 'POST':
        form_orcamento = OrcamentoVendaForm(request.POST,instance=orcamento)                
        if form_orcamento.is_valid():
            form_orcamento.save()
            orcamento_id = id
            return redirect('oficina:novo_item',orcamento_id=orcamento_id)            
    elif request.method == 'GET':        
        return render(request,'oficina/vendas/atualizarOrcamentoVenda.html',data)

def detail_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(OrcamentoVenda,pk=orcamento_id)        
    lista_itens = ItemVenda.objects.filter(orcamento=orcamento_id).order_by('produto')    
    data = {
        'lista_itens':lista_itens,        
        'orcamento':orcamento,
    }
    return render(request,'oficina/vendas/detail.html',data)


############### Registrar usuarios ######################
class register(generic.CreateView):
    form_class = UserCreationForm
    #success_url = reverse_lazy('login')
    template_name = 'oficina/register.html'

#####################################################
def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


######################

def search_status(request):

    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            statuss = Produto.objects.filter(descricao__contains = search_text)
        else:
            statuss = []

        return render(request, 'teste.html', {'statuss':statuss})
