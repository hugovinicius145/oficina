# Generated by Django 2.2.3 on 2019-07-06 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0013_auto_20190702_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemvenda',
            name='numero_item',
        ),
        migrations.AlterField(
            model_name='itemvenda',
            name='preco',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço'),
        ),
    ]
