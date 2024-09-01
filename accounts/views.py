from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from .models import DadosAnimal, Medicamento, Procedimento
from .forms import CustomUserCreationForm, DadosAnimalForm, MedicamentoForm, ProcedimentoForm
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

def read(request):
    dic = {}
    dic['dados_animal'] = DadosAnimal.objects.all()
    dic['dados_medicamento'] = Medicamento.objects.all()
    dic['dados_procedimento'] = Procedimento.objects.all()
    return render(request, 'registration/read.html', dic)

def cadastro_animal(request):
    dic = {}
    form = DadosAnimalForm(request.POST or None)
    if form.is_valid():
        form.save()
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
    animal = DadosAnimal.objects.get(pk=pk)
    animal.delete()
    return redirect('read')


def cadastro_medicamento(request):
    dic = {}
    form = MedicamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
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
    medicamento = Medicamento.objects.get(pk=pk)
    medicamento.delete()
    return redirect('read')

def cadastro_procedimento(request):
    dic = {}
    form = ProcedimentoForm(request.POST or None)
    if form.is_valid():
        form.save()
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
    procedimento = Procedimento.objects.get(pk=pk)
    procedimento.delete()
    return redirect('read')

    
        