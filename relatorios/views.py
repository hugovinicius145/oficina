from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from .models import *
from oficina.models import *
#from .forms import *
from urllib.parse import urlencode
from .forms import *
from django.utils import timezone
from datetime import datetime
import pytz
from dateutil import tz


# Create your views here.
def index(request):
    return render(request, "relatorios/index.html")

def lucro(request):
    periodo = request.GET.get('periodo')
    lista = OrcamentoVenda.objects.all()

    total = 0
    lista2 =[]
    for item in lista:
        if '2019-07-21' in str(item.modified):
            lista2.append(item)
    data = {'lista':lista2}
    return render(request,'relatorios/lucro.html',data)
def total_vendido(request):
    periodo = request.GET.get('periodo')
    form = myDateForm()
    base_url = '/relatorios/total/vendas'
    data_inicial = str(periodo)[0:10]
    data_final = str(periodo)[10:]

    data = data_inicial[6:10] + '-' + data_inicial[3:5]
    

    if (request.method == 'POST'):
        form = myDateForm(request.POST)
        if form.is_valid():
            dataInicial = form.cleaned_data['dataInicial']
            dataFinal = form.cleaned_data['dataFinal']
            query_string = urlencode({'periodo':dataInicial + dataFinal})            
            url = '{}?{}'.format(base_url,query_string)
            return redirect(url)
    if (request.method == 'GET'):
        return render(request,'relatorios/estoque/itensVendidos.html',data)
        
def itens_vendidos(request):    
    periodo = request.GET.get('periodo')
    form = myDateForm()
    base_url = '/relatorios/itens'

    lista_orcamentos = OrcamentoVenda.objects.all()
    lista_final = []
    for orcamento in lista_orcamentos:
        if get_data_inicial(periodo) in mudar_horario(orcamento.modified):
           lista_final.append(orcamento.get_itens_vendidos())

    data = {
        'form':form,
        'lista_orcamentos':lista_orcamentos,
        'lista_final':lista_final,
        'periodo':data_valida("01/02/2019"),
    }
    
    if (request.method == 'POST'):
        form = myDateForm(request.POST)
        if form.is_valid():
            dataInicial = form.cleaned_data['dataInicial']
            dataFinal = form.cleaned_data['dataFinal']
            query_string = urlencode({'periodo':dataInicial + dataFinal})            
            url = '{}?{}'.format(base_url,query_string)
            return redirect(url)
    if (request.method == 'GET'):
        return render(request,'relatorios/estoque/itensVendidos.html',data)

##### Pedidos #####################################


def pedidos(request):
    form = ItemPedidoForm()
    lista_itens = ItemPedido.objects.all().order_by('descricao')
    data = {
        'form':form,
        'lista_itens':lista_itens,
        }
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('relatorios:pedidos')
    elif request.method == 'GET':  
        return render(request, "relatorios/pedidos/index.html",data)

def apagar_pedido(request,item_id):
    item_pedido = get_object_or_404(ItemPedido,pk=item_id)
    item_pedido.delete()
    return redirect('relatorios:pedidos')

def atualizar_pedido(request,id):
    item = get_object_or_404(ItemPedido,pk=id)
    form = ItemPedidoForm(instance=item)
    data = {
        'form':form,        
    }
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('relatorios:pedidos')
    elif request.method == 'GET':        
        return render(request,'relatorios/pedidos/edit.html',data)

      
######## Funcoes Auxiliares  ######################################################
         
def mudar_horario(data_banco):
    horario_banco = str(data_banco)[0:19]

    zona_utc = tz.gettz('UTC')
    zona_br = tz.gettz('America/Sao_Paulo')

    utc = datetime.strptime(horario_banco, '%Y-%m-%d %H:%M:%S')    
    utc = utc.replace(tzinfo=zona_utc)
    br = utc.astimezone(zona_br)
    return str(br)

def get_data_inicial(periodo):
    periodo = str(periodo)
    return periodo[6:10] + '-' + periodo[3:5] + '-' + periodo[0:2]


def get_data_final(periodo):
    periodo = str(periodo)
    return periodo[16:20] + '-' + periodo[13:15] + '-' + periodo[10:12]

def ano_valido(ano):
    if ano > 1900 and ano < 2300:
        return True
    else:
        return False

def mes_valido(mes):
    if mes > 0 and mes <13:
        return True
    else:
        return False

def data_valida(data):
    # 23/03/2019
    ano = int(get_data_inicial(data)[0:4])
    mes = int(get_data_inicial(data)[5:7])
    dia = int(get_data_inicial(data)[8:10])    

    if ano_valido(ano):
        if mes_valido(mes):
            if mes in [1,3,5,7,8,10,12]:
                if dia > 0 and dia < 32:
                    return True
            if mes in [4,6,9,11]:
                if dia > 0 and dia < 31:
                    return True
            if mes == 2:            
                if ano % 4 == 0:
                    if ano % 100 == 0:
                        if dia > 0 and dia < 29:
                            return True
                    else:
                        if dia > 0 and dia < 30:
                            return True  
                else:
                    if dia > 0 and dia < 29:
                            return True        



'''def set_datas(periodo,lista):
    lista_final = []

    ano_inicial = int(get_data_inicial(periodo)[0:4])
    ano_final = int(get_data_final(periodo)[0:4])

    mes_inicial = int(get_data_inicial(periodo)[5:7])
    mes_final = int(get_data_final(periodo)[5:7])

    dia_inicial = int(get_data_inicial(periodo)[8:10])
    dia_final = int(get_data_final(periodo)[8:0])

    inicio = int(get_data_inicial(periodo)[8:10])
    final = int(get_data_final(periodo)[8:10])

    cont_ano = 0
    cont_mes = 0
    cont_dia = 0
    if ano_inicial <= ano_final:
        cont_ano = cont_ano + (ano_final - ano_inicial)
        if mes_inicial <= mes_final:
            cont_mes = cont_mes + (mes_final - mes_inicial)
            if dia_inicial <= dia_final:
                cont_dia = cont_dia + (dia_final - dia_inicial)
                data_valida = True
            else:
                return False
        else:
            return False
    else:
        return False
    # if inicio <= final:

    for item in lista:
        if get_data_inicial(periodo) in mudar_horario(item.modified):
           lista_final.append(item.get_itens_vendidos())
    return True'''
#inicial_data = data_inicial[6:10] + '-' + data_inicial[3:5] + '-' + data_inicial[0:2] + " 00:00:00"