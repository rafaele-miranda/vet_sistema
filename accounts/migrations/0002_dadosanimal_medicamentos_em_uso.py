# Generated by Django 5.1.5 on 2025-02-24 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosanimal',
            name='medicamentos_em_uso',
            field=models.ManyToManyField(blank=True, to='accounts.medicamento'),
        ),
    ]
