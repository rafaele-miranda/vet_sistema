# Generated by Django 5.1.5 on 2025-02-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_procedimento_tipo_procedimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosanimal',
            name='status_saude',
            field=models.CharField(choices=[('saudavel', 'Saudável'), ('em_tratamento', 'Em Tratamento'), ('condicao_cronica', 'Condição Crônica')], default='saudavel', max_length=100),
        ),
    ]
