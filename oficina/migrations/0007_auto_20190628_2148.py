# Generated by Django 2.2.2 on 2019-06-29 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0006_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
