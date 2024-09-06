from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator

proced = [
      ('vacinacao', 'Vacinação'),
      ('castracao', 'Castração'),
      ('lab', 'Exames laboratoriais'),
      ('imagem', 'Exames de imagem'),
      ('tumor', 'Remoção de tumores'),
      ('limpeza', 'Limpeza dental'),
      ('cirurgia', 'Cirurgia'),
    ]

class CustomUser(AbstractUser):
  groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
  user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
  
  
class DadosAnimal(models.Model):
    
    sexo = [
    ('m', 'M'),
    ('f', 'F'),
    ]
    
    chip = [
        ('s', 'SIM'),
        ('n', 'NÃO'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo_animal = models.CharField(max_length=100)
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=100, choices=sexo, default='1')
    nascimento = models.DateTimeField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    cor = models.CharField(max_length=100)
    microchip = models.CharField(max_length=100, choices=chip, default='1')
    data_entrada = models.DateTimeField()
    tutor = models.CharField(max_length=100)
    telefone = models.CharField( max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    endereco = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome


class Medicamento(models.Model):
  medicamento = models.CharField(max_length=100)
  frequecia = models.CharField(max_length=100, verbose_name='Frequência')
  dosagem = models.CharField(max_length=100)
  duracao = models.CharField(max_length=100, verbose_name='Duração')
  observacoes = models.CharField(max_length=100, verbose_name='Observações')
  
  animal = models.ForeignKey(DadosAnimal, on_delete=models.CASCADE, related_name='medicamentos', default='1', null=True, blank=True)
  
  def __str__(self):
      return self.medicamento
    

class Procedimento(models.Model):
  tipo_procedimento = models.CharField(max_length=100, choices=proced, default='1')
  data = models.DateTimeField()
  veterinario_responsavel = models.CharField(max_length=100, verbose_name='Veterinário ')
  observacao = models.CharField(max_length=100, verbose_name='Observação')
  
  animal = models.ForeignKey(DadosAnimal, on_delete=models.CASCADE, related_name='procedimentos', default='1')
  
  def __str__(self):
    return self.tipo_procedimento