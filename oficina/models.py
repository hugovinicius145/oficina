from django.db import models
import datetime
class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
class Produto(models.Model):
    descricao = models.CharField(max_length=255,unique=True)
    quantidade = models.IntegerField()
    valor_compra = models.DecimalField(max_digits=9, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(to=Categoria, on_delete=models.CASCADE, blank=True, null=True)
    codigo_fabrica = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['descricao']

    def __str__(self):
        txt = '{} | QTD: {} | Preço: R${}'.format(self.descricao,self.quantidade,self.valor_venda)
        return txt

    def get_valor_venda(self):
        return self.valor_venda
    
    def baixar_estoque(self,quantidade):
        if (self.quantidade - quantidade) >= 0:        
            self.quantidade = self.quantidade - quantidade
            return True
        else:
            return False
            

class Endereco(models.Model):
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=5)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    ESTADOS_CHOICES = (
        ("AC","Acre"),("AL","Alagoas"),  ("AM","Amazonas"),("AP","Amapá"),("BA","Bahia"),("CE","Ceará"),("DF","Distrito Federal"),("ES","Espírito Santo"),("GO","Goiás"),("MA","Maranhão"),("MG","Minas Gerais"),("MS","Mato Grosso do Sul"),("MT","Mato Grosso"),("PA","Pará"),("PB","Paraíba"),("PE","Pernambuco"),("PI","Piauí"),("PR","Paraná"),("RJ","Rio de Janeiro"),("RN","Rio Grande do Norte"),("RO","Rondônia"),("RR","Roraima"),("RS","Rio Grande do Sul"),("SC","Santa Catarina"),("SE","Sergipe"),("SP","São Paulo"),("TO","Tocantins")
    )
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES)

class Telefone(models.Model):
    telefone = models.CharField(max_length=255)    
    def get_id(self):
        return self.id
    def __str__(self):
        return self.telefone
        

class Fornecedor(models.Model):
    descricao = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    observacao = models.CharField(max_length=255,blank=True, null=True)
    telefone = models.OneToOneField(Telefone,on_delete=models.SET_NULL,null=True)
    def get_endereco(self):
        return self.endereco.id
    def __str__(self):
        return self.descricao
    def get_telefone(self):
        return self.telefone.id

class Servico(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.descricao

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=255,blank=True, null=True)
    telefone = models.OneToOneField(Telefone, on_delete=models.SET_NULL, null=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = (
        ("+","Positivo"),("-","Negativo"),("0","Nulo")
    )
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default="Nulo")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nome
    
    def get_endereco(self):
        return self.endereco.id
    def get_telefone(self):
        return self.telefone.id

class OrcamentoVenda(models.Model):
    TIPO_CHOICES = (
        ("DINHEIRO","DINHEIRO"),("CARTÂO","CARTÂO"),("PRAZO","PRAZO")
    )
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE,blank=True, null=True)
    vendedor = models.CharField(max_length=255, null=True)
    status = models.BooleanField()    
    desconto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-created']
    
    def numero_itens(self):       
       itens = ItemVenda.objects.filter(orcamento=self.id)
       total = 0
       for item in itens:
           total = total + item.quantidade
       return total

    def get_itens(self):
        lista = ItemVenda.objects.filter(orcamento=self.id)
        s = ""
        for l in lista:
            s = s + str(l) +""
        return s

    def preco_total(self):
        if self.desconto == None:
            return self.get_preco_subtotal() - 0
        elif (self.get_preco_subtotal() - self.desconto) >= 0:
            return self.get_preco_subtotal() - self.desconto

    def get_preco_subtotal(self):
        itens = ItemVenda.objects.filter(orcamento=self.id)
        total = 0
        for item in itens:
            total = total + item.get_preco_total()
        return total
        
class Venda(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    orcamento = models.OneToOneField(OrcamentoVenda, on_delete=models.SET_NULL,null=True)

class ItemVenda(models.Model):
    servico = models.ForeignKey("Servico",on_delete=models.CASCADE,blank=True, null=True)
    produto = models.ForeignKey("Produto",on_delete=models.CASCADE,blank=True, null=True)    
    orcamento = models.ForeignKey("OrcamentoVenda",on_delete=models.CASCADE,blank=True, null=True)
    quantidade = models.IntegerField()
    
    def __str__(self):
        if self.servico != None:
            return str(self.servico)
        if self.produto != None:
            return str(self.produto)

    def get_preco_und(self):
        if self.produto != None:
            return (self.produto.valor_venda)
        elif self.servico != None:
            return (self.servico.valor)
            
    def get_preco_total(self):
        if self.produto != None:
            return (self.produto.valor_venda * self.quantidade)
        elif self.servico != None:
            return (self.servico.valor * self.quantidade)

'''
class ItemCaixa(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    despesa = models.CharField(max_length=255, null=True, blank=True)


class Caixa(models.Model):
    created = models.DateTimeField(auto_now_add=True)
'''