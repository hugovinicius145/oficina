# Generated by Django 2.2.2 on 2019-06-29 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0008_auto_20190629_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='telefones',
            field=models.ManyToManyField(blank=True, null=True, to='oficina.Telefone'),
        ),
    ]
