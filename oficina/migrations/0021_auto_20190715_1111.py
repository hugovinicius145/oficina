# Generated by Django 2.2.3 on 2019-07-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0020_auto_20190709_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedor',
            name='cnpj',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='telefone',
            field=models.CharField(max_length=255),
        ),
    ]
