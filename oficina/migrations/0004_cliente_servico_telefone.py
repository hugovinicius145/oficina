# Generated by Django 2.2.2 on 2019-06-28 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0003_endereco_fornecedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=11)),
                ('status', models.CharField(choices=[('+', 'Positivo'), ('-', 'Negativo'), ('0', 'Nulo')], max_length=1)),
                ('endereco_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oficina.Endereco')),
                ('telefones', models.ManyToManyField(to='oficina.Telefone')),
            ],
        ),
    ]
