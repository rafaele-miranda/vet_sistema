from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .models import DadosAnimal, Medicamento, Procedimento
from .forms import CustomUserCreationForm, DadosAnimalForm, MedicamentoForm, ProcedimentoForm
from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html')

def home(request):
    return render(request, 'registration/home.html')

@login_required
def read(request):
    dic = {}
    dic['dados_animal'] = DadosAnimal.objects.all()
    dic['dados_medicamento'] = Medicamento.objects.all()
    dic['dados_procedimento'] = Procedimento.objects.all()
    return render(request, 'registration/read.html', dic)

@login_required
def cadastro_animal(request):
    dic = {}
    message = "Paciente adicionado com sucesso!"
    form = DadosAnimalForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, message)
        return redirect('read')
    
    dic['form'] = form
    return render(request, 'registration/form.html', dic)

def update(request, pk):
    animal = DadosAnimal.objects.get(pk=pk)
    form = DadosAnimalForm(request.POST or None, instance=animal)
    
    if form.is_valid():
        form.save()
        return redirect('read')
    
    dic = {}
    dic['form'] = form
    dic['animal'] = animal
    return render(request, 'registration/form.html', dic)

def delete(request, pk):
    message = "Paciente removido com sucesso!"
    animal = DadosAnimal.objects.get(pk=pk)
    animal.delete()
    messages.warning(request, message)
    return redirect('read')

@login_required
def cadastro_medicamento(request):
    dic = {}
    message = "Medicamento adicionado com sucesso!"
    form = MedicamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, message)
        return redirect('read')
    dic['form'] = form
    return render(request, 'registration/form_medicamento.html', dic)

def update_medicamento(request, pk):
    animal = Medicamento.objects.get(pk=pk)
    form = MedicamentoForm(request.POST or None, instance=animal)
    if form.is_valid():
        form.save()
        return redirect('read')
    
    dic = {}
    dic['form'] = form
    dic['animal'] = animal
    return render(request, 'registration/form_medicamento.html', dic)
        
def deleteMedicamento(request, pk):
    message = "Medicamento removido com sucesso!"
    medicamento = Medicamento.objects.get(pk=pk)
    medicamento.delete()
    messages.warning(request, message)
    return redirect('read')

@login_required
def cadastro_procedimento(request):
    dic = {}
    message = "Procedimento adicionado com sucesso!"
    form = ProcedimentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, message)
        return redirect('read')
    dic['form'] = form
    return render(request, 'registration/form_procedimento.html', dic)

def update_procedimento(request, pk):
    animal = Procedimento.objects.get(pk=pk)
    form = ProcedimentoForm(request.POST or None, instance=animal)
    dic = {}
    
    if form.is_valid():
        form.save()
        return redirect('read')
    
    dic['form'] = form
    dic['animal'] = animal
    return render(request, 'registration/form_procedimento.html', dic)

def deleteProcedimento(request, pk):
    message = "Procedimento removido com sucesso!"
    procedimento = Procedimento.objects.get(pk=pk)
    procedimento.delete()
    messages.warning(request, message)
    return redirect('read')

def animal_relatorio(request):
    animal_id = request.GET.get('animal_id') 
    if animal_id:
        animal = get_object_or_404(DadosAnimal, id=animal_id)
        medicamentos = animal.medicamentos.all()
        procedimentos = animal.procedimentos.all()

        context = {
            'animal': animal,
            'medicamentos': medicamentos,
            'procedimentos': procedimentos,
        }

        return render(request, 'relatorio.html', context)
    else:
        return redirect('read')  
        
def timeout_view(request):
    return render(request, 'timeout.html')