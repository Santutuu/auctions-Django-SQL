# Generated by Django 5.0.6 on 2024-09-04 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_subastas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subastas',
            name='imagen',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='subastas',
            name='ofertaInicial',
            field=models.IntegerField(),
        ),
    ]
