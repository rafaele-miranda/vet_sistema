from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser, DadosAnimal, Medicamento, Procedimento, EstoqueMedicamento

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        

class DadosAnimalForm(ModelForm):
    class Meta:
        model = DadosAnimal
        fields = '__all__'
      
class MedicamentoForm(ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
    

class ProcedimentoForm(ModelForm):
    class Meta:
        model = Procedimento
        fields = '__all__'
        
class EstoqueMedicamentoForm(forms.ModelForm):
    class Meta:
        model = EstoqueMedicamento
        fields = ['nome', 'dosagem', 'descricao', 'quantidade', 'estoque_minimo']