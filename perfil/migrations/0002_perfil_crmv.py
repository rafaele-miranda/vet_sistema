# Generated by Django 5.0.2 on 2025-04-01 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='crmv',
            field=models.CharField(blank=True, max_length=100, verbose_name='CRMV'),
        ),
    ]
