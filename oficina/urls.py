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
    #path('login/', views.login, name='login'),
    #path('welcome/', views.welcome, name='welcome'),
]