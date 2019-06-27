from django.db import models

class Produto(models.Model):
    descricao = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    valor_compra = models.DecimalField(max_digits=9, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def __str__(self):
        return self.descricao

class Endereco(models.Model):
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=5)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True)
    ESTADOS_CHOICES = (
        ("AC","Acre"),("AL","Alagoas"),  ("AM","Amazonas"),("AP","Amapá"),("BA","Bahia"),("CE","Ceará"),("DF","Distrito Federal"),("ES","Espírito Santo"),("GO","Goiás"),("MA","Maranhão"),("MG","Minas Gerais"),("MS","Mato Grosso do Sul"),("MT","Mato Grosso"),("PA","Pará"),("PB","Paraíba"),("PE","Pernambuco"),("PI","Piauí"),("PR","Paraná"),("RJ","Rio de Janeiro"),("RN","Rio Grande do Norte"),("RO","Rondônia"),("RR","Roraima"),("RS","Rio Grande do Sul"),("SC","Santa Catarina"),("SE","Sergipe"),("SP","São Paulo"),("TO","Tocantins")
    )
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES)
    def __str__(self):
        return self.logradouro

class Fornecedor(models.Model):
    descricao = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, blank=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    observacao = models.CharField(max_length=255)
    
    def get_endereco(self):
        return self.endereco
    def __str__(self):
        return self.descricao

