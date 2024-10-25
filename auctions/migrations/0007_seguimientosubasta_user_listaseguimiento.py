# Generated by Django 5.0.6 on 2024-10-22 14:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_subastas_creador'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeguimientoSubasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_seguido', models.BooleanField(default=False)),
                ('subasta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.subastas')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='listaSeguimiento',
            field=models.ManyToManyField(through='auctions.SeguimientoSubasta', to='auctions.subastas'),
        ),
    ]