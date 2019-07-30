from django.urls import path, include
from django.conf.urls import url

from . import views
app_name = 'relatorios'
urlpatterns = [    
    path('lucro/', views.lucro, name='lucro'),
    path('itens/', views.itens_vendidos, name='itens_vendidos'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/delete/<int:item_id>', views.apagar_pedido, name='apagar_pedido'),
    path('pedidos/edit/<int:id>', views.atualizar_pedido, name='atualizar_pedido'),
]   