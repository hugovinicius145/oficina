# Generated by Django 2.2.3 on 2019-08-04 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0023_produto_estoque_minimo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='estoque_minimo',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
