# Generated by Django 2.2.3 on 2019-07-30 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0002_remove_itempedido_pedido'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pedido',
        ),
    ]
