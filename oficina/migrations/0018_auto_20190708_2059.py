# Generated by Django 2.2.3 on 2019-07-08 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0017_auto_20190708_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemvenda',
            name='status',
        ),
        migrations.AddField(
            model_name='orcamentovenda',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]