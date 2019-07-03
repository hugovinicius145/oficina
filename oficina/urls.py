from django.urls import path

from . import views
app_name = 'oficina'
urlpatterns = [
    path('', views.index, name='index'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/new/', views.novo_produto, name='novo_produto'),
    path('produtos/delete/<int:id>/', views.apagar_produto, name='apagar_produto'),
    path('produtos/update/<int:id>/', views.atualizar_produto, name='atualizar_produto'),
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/new', views.novo_fornecedor, name='novo_fornecedor'),
    path('fornecedores/delete/<int:id>/', views.apagar_fornecedor, name='apagar_fornecedor'),
    path('fornecedores/edit/<int:id>/', views.atualizar_fornecedor, name='atualizar_fornecedor'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/new', views.novo_cliente, name='novo_cliente'),
    path('clientes/edit/<int:id>/', views.atualizar_cliente, name='atualizar_cliente'),
    path('clientes/delete/<int:id>/', views.apagar_cliente, name='apagar_cliente'),
    path('servicos/', views.servicos, name='servicos'),
    path('servicos/new', views.novo_servico, name='novo_servico'),
    path('servicos/delete/<int:id>/', views.apagar_servico, name='apagar_servico'),
    path('servicos/edit/<int:id>/', views.atualizar_servico, name='atualizar_servico'),
    #path('vendas/', views.vendas, name='vendas'),
    path('vendas/new', views.nova_venda, name='nova_venda'),
    #path('vendas/edit/<int:id>/', views.atualizar_venda, name='atualizar_venda'),

]
