from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator




class CustomUser(AbstractUser):
  groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
  user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
  
  
class DadosAnimal(models.Model):
    
    sexo = [
    ('m', 'M'),
    ('f', 'F'),
    ]
    
    castrado = [
        ('s', 'SIM'),
        ('n', 'NÃO'),
    ]
    
    chip = [
        ('s', 'SIM'),
        ('n', 'NÃO'),
    ]
    
    status_saude = [
        ('saudavel', 'Saudável'),
        ('em_tratamento', 'Em Tratamento'),
        ('condicao_cronica', 'Condição Crônica'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo_animal = models.CharField(max_length=100)
    raca = models.CharField(max_length=100)
    sexo = models.CharField(max_length=100, choices=sexo, default='1')
    nascimento = models.DateTimeField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    cor = models.CharField(max_length=100)
    microchip = models.CharField(max_length=100, choices=chip, default='1')
    castrado = models.CharField(max_length=100, choices=castrado, default=1)
    data_entrada = models.DateTimeField()
    tutor = models.CharField(max_length=100)
    telefone = models.CharField( max_length=15, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')])
    endereco = models.CharField(max_length=100)
    status_saude = models.CharField(max_length=100, choices=status_saude, default='saudavel') 

    
    def __str__(self):
        return self.nome

class EstoqueMedicamento(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Medicamento')
    dosagem = models.CharField(max_length=100, verbose_name='Dosagem')
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=0, verbose_name='Quantidade em Estoque')
    estoque_minimo = models.PositiveIntegerField(default=10, verbose_name='Estoque Mínimo')

    def __str__(self):
        return f"{self.nome} ({self.dosagem})"

    def em_falta(self):
        return self.quantidade <= self.estoque_minimo

class Medicamento(models.Model):
    estoque_medicamento = models.ForeignKey('EstoqueMedicamento', on_delete=models.CASCADE, related_name='medicamentos_estoque', verbose_name='Medicamento em Estoque')
    frequencia = models.CharField(max_length=100, verbose_name='Frequência')
    dosagem = models.CharField(max_length=100)
    duracao = models.CharField(max_length=100, verbose_name='Duração')
    observacoes = models.CharField(max_length=100, verbose_name='Observações')
    via_administracao = models.CharField(max_length=100, verbose_name="Via de Administração", default="VO")
    data_hora_administracao = models.DateTimeField(verbose_name="Data/Hora de Administração",null=True, blank=True)

    animal = models.ForeignKey('DadosAnimal', on_delete=models.CASCADE, related_name='medicamentos', default='1', null=True, blank=True)

    def __str__(self):
        return f"{self.estoque_medicamento.nome} - {self.frequencia}"
    

class Procedimento(models.Model):
  procedimento = [
      ('vacinacao', 'Vacinação'),
      ('castracao', 'Castração'),
      ('lab', 'Exames laboratoriais'),
      ('imagem', 'Exames de imagem'),
      ('tumor', 'Remoção de tumores'),
      ('limpeza', 'Limpeza dental'),
      ('cirurgia', 'Cirurgia'),
    ]
  tipo_procedimento = models.CharField(max_length=100, choices=procedimento, default='1')
  data = models.DateTimeField()
  veterinario_responsavel = models.CharField(max_length=100, verbose_name='Veterinário responsável')
  observacao = models.CharField(max_length=100, verbose_name='Observação')
  
  animal = models.ForeignKey(DadosAnimal, on_delete=models.CASCADE, related_name='procedimentos', default='1')
  
  def __str__(self):
    return self.tipo_procedimento
  
  


  
  
