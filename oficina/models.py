from django.db import models
class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
class Produto(models.Model):
    descricao = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    valor_compra = models.DecimalField(max_digits=9, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(to=Categoria, on_delete=models.CASCADE, blank=True, null=True)
    codigo_fabrica = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.descricao

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
    telefone = models.CharField(max_length=20)    
    def get_id(self):
        return self.id
    def __str__(self):
        return self.telefone
        

class Fornecedor(models.Model):
    descricao = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, blank=True, null=True)
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
    cpf = models.CharField(max_length=11,blank=True, null=True)
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

class Venda(models.Model):
    TIPO_CHOICES = (
        ("DINHEIRO","DINHEIRO"),("CARTÂO","CARTÂO"),("PRAZO","PRAZO")
    )
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE,blank=True, null=True)
    vendedor = models.CharField(max_length=255)    
    
    class Meta:
        ordering = ['-created']
    
    def numero_itens(self):       
       lista = []
       lista.append(ItemVenda.objects.filter(venda=self.id))
       return len(lista)

class ItemVenda(models.Model):
    servico = models.ForeignKey("Servico",on_delete=models.CASCADE,blank=True, null=True)
    produto = models.ForeignKey("Produto",on_delete=models.CASCADE,blank=True, null=True)
    venda = models.ForeignKey("Venda",on_delete=models.CASCADE)
    quantidade = models.IntegerField()    
    numero_item = models.IntegerField(verbose_name='Nº do Item', editable=False)
    preco = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2)
    item_cancelado = models.BooleanField(verbose_name='Item cancelado', default=False)

    