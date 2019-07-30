from django.db import models

class ItemPedido(models.Model):
    descricao = models.CharField(max_length=255)
    quantidade = models.IntegerField()    
        
    def __str__(self):
        return str(self.descricao)
