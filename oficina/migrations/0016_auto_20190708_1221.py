# Generated by Django 2.2.3 on 2019-07-08 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0015_auto_20190707_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orcamentovenda',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='venda',
            options={},
        ),
        migrations.RemoveField(
            model_name='itemvenda',
            name='venda',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='vendedor',
        ),
        migrations.AddField(
            model_name='orcamentovenda',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oficina.Cliente'),
        ),
        migrations.AddField(
            model_name='orcamentovenda',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='orcamentovenda',
            name='tipo',
            field=models.CharField(choices=[('DINHEIRO', 'DINHEIRO'), ('CARTÂO', 'CARTÂO'), ('PRAZO', 'PRAZO')], max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='orcamentovenda',
            name='vendedor',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='orcamento',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oficina.OrcamentoVenda'),
        ),
    ]
