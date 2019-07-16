from django.urls import path, include
from django.conf.urls import url

from . import views
app_name = 'oficina'
urlpatterns = [
    path('', views.index, name='index'),   
    path('register/', views.register, name='register'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/new/', views.novo_produto, name='novo_produto'),
    path('produtos/delete/<int:id>/', views.apagar_produto, name='apagar_produto'),
    path('produtos/update/<int:id>/', views.atualizar_produto, name='atualizar_produto'),
    path('produtos/validar/', views.validar_descricao_produto, name='validar_descricao_produto'),
    #####################################
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/new', views.novo_fornecedor, name='novo_fornecedor'),
    path('fornecedores/delete/<int:id>/', views.apagar_fornecedor, name='apagar_fornecedor'),
    path('fornecedores/edit/<int:id>/', views.atualizar_fornecedor, name='atualizar_fornecedor'),
    #######################################
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/new', views.novo_cliente, name='novo_cliente'),
    path('clientes/edit/<int:id>/', views.atualizar_cliente, name='atualizar_cliente'),
    path('clientes/delete/<int:id>/', views.apagar_cliente, name='apagar_cliente'),
    #######################################
    path('servicos/', views.servicos, name='servicos'),
    path('servicos/new', views.novo_servico, name='novo_servico'),
    path('servicos/delete/<int:id>/', views.apagar_servico, name='apagar_servico'),
    path('servicos/edit/<int:id>/', views.atualizar_servico, name='atualizar_servico'),
    #######################################
    path('vendas/', views.vendas, name='vendas'),
    path('vendas/detail/<int:orcamento_id>/', views.detail_orcamento, name='detail_orcamento'),    
    path('orcamentos/', views.orcamentos, name='orcamentos'),
    path('orcamentos/delete/<int:id>/', views.apagar_orcamento, name='apagar_orcamento'),
    path('orcamentos/edit/<int:id>/', views.atualizar_orcamento, name='atualizar_orcamento'),
    path('vendas/new', views.nova_venda, name='nova_venda'),    
    path('vendas/add/item/<int:orcamento_id>/', views.novo_item, name='novo_item'),
    path('vendas/delete/item/<int:orcamento_id>/<int:id>/', views.apagar_item, name='apagar_item'),
    path('vendas/edit/item/<int:orcamento_id>/<int:id>/', views.atualizar_item, name='atualizar_item'),
    path('vendas/finish/<int:orcamento_id>/', views.finalizar_venda, name='finalizar_venda'),
]
