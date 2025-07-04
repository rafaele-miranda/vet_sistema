from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.conf import settings
from django.conf import settings
from .models import DadosAnimal, Medicamento, Procedimento, EstoqueMedicamento
from .forms import CustomUserCreationForm, DadosAnimalForm, MedicamentoForm, ProcedimentoForm, EstoqueMedicamentoForm
from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from django.db.models import Count
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.utils import filtrar_modelo

from accounts import models


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    

@login_required
def dashboard(request):
    total_animais = DadosAnimal.objects.count()
    total_medicamentos = EstoqueMedicamento.objects.count()  
    total_procedimentos = Procedimento.objects.count()
    
    animais_saudaveis = DadosAnimal.objects.filter(status_saude='saudavel').count()
    animais_em_tratamento = DadosAnimal.objects.filter(status_saude='em_tratamento').count()
    animais_condicao_cronica = DadosAnimal.objects.filter(status_saude='condicao_cronica').count()
    
    medicamentos_mais_utilizados = Medicamento.objects.values('estoque_medicamento__nome').annotate(total_uso=Count('animal')).order_by('-total_uso')[:3]
    medicamentos_em_falta = EstoqueMedicamento.objects.filter(quantidade__lte=10)  
   
    context = {
        'total_animais': total_animais,
        'total_medicamentos': total_medicamentos,
        'total_procedimentos': total_procedimentos,
        'animais_saudaveis': animais_saudaveis,
        'animais_em_tratamento': animais_em_tratamento,
        'animais_condicao_cronica': animais_condicao_cronica,
        'medicamentos_mais_utilizados': medicamentos_mais_utilizados,  
        'medicamentos_em_falta': medicamentos_em_falta,
    }
    
    return render(request, 'registration/dashboard.html', context)

def home(request):
    return render(request, 'registration/home.html')

@login_required
def read(request):
    dic = {}
    nome_busca = request.GET.get("nome")

    # Filtro para DadosAnimal (busca direta pelo nome)
    dados_animal = models.DadosAnimal.objects.all()
    if nome_busca:
        dados_animal = dados_animal.filter(nome__icontains=nome_busca)

    # Filtro para Medicamento (busca pelo nome do animal relacionado)
    dados_medicamento = models.Medicamento.objects.all()
    if nome_busca:
        dados_medicamento = dados_medicamento.filter(animal__nome__icontains=nome_busca)

    # Filtro para Procedimento (busca pelo nome do animal relacionado)
    dados_procedimento = models.Procedimento.objects.all()
    if nome_busca:
        dados_procedimento = dados_procedimento.filter(animal__nome__icontains=nome_busca)

    dic.update({
        'dados_animal': dados_animal,
        'dados_medicamento': dados_medicamento,
        'dados_procedimento': dados_procedimento
    })
    
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


@login_required
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


@login_required
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


@login_required
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


@login_required        
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


@login_required
def update_procedimento(request, pk):
    animal = Procedimento.objects.get(pk=pk)
    form = ProcedimentoForm(request.POST or None, instance=animal)
    
    if form.is_valid():
        form.save()
        return redirect('read')
    
    dic = {}
    dic['form'] = form
    dic['animal'] = animal
    return render(request, 'registration/form_procedimento.html', dic)

@login_required
def deleteProcedimento(request, pk):
    message = "Procedimento removido com sucesso!"
    procedimento = Procedimento.objects.get(pk=pk)
    procedimento.delete()
    messages.warning(request, message)
    return redirect('read')
 
class RelatorioPDFAPIView(APIView):
    def get(self, request, animal_id):
        try:
            animal = get_object_or_404(DadosAnimal, id=animal_id)
            html_string = render_to_string('relatorio.html', {
                'request': request,
                'animal': animal,
                'medicamentos': animal.medicamentos.all(),
                'procedimentos': animal.procedimentos.all()
            })

            # Configurações para o WeasyPrint
            pdf = HTML(
                string=html_string,
                base_url=request.build_absolute_uri('/')
            ).write_pdf()

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="relatorio_{animal.nome}.pdf"'
            return response

        except Exception as e:
            print(f"Erro na geração do PDF: {str(e)}")
            return HttpResponse(
                f"Erro ao gerar PDF: {str(e)}", 
                status=500,
                content_type='text/plain'
            )
        
def timeout_view(request):
    return render(request, 'timeout.html')

def api_view(request):
    raca_name = request.GET.get("raca_name", "") 
    raca_info = None
    error = None

    if raca_name:
        api_key = settings.API_KEY 
        url = f"https://api.thedogapi.com/v1/breeds/search?q={raca_name}"
        headers = {"x-api-key": api_key}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                raca_info = data[0]  
            else:
                error = "Raça não encontrada."
        else:
            error = f"Erro ao acessar a API. Código: {response.status_code}"

    return render(request, "api.html", {"raca_info": raca_info, "error": error})

@login_required
def adicionar_estoque(request):
    if request.method == 'POST':
        form = EstoqueMedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_estoque')
    else:
        form = EstoqueMedicamentoForm()
    
    context = {'form': form}
    return render(request, 'adicionar_estoque.html', context)


@login_required
def listar_estoque(request):
    estoques = EstoqueMedicamento.objects.all()  
    context = {'estoques': estoques}
    return render(request, 'listar_estoque.html', context)


@login_required
def excluir_estoque(request, estoque_id):
    estoque = get_object_or_404(EstoqueMedicamento, id=estoque_id)
    estoque.delete()
    messages.success(request, 'Medicamento excluído com sucesso!')
    return redirect('listar_estoque')



