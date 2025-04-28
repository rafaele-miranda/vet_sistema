from .views import SignUpView
from django.urls import path
from . import views
from .views import RelatorioPDFAPIView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('read/', views.read, name='read'),
    path('cadastro/', views.cadastro_animal, name='cadastro'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('cadastro_medicamento/', views.cadastro_medicamento, name='cadastro_medicamento'),
    path('update_medicamento/<int:pk>/', views.update_medicamento, name='update_medicamento'),
    path('delete_medicamento/<int:pk>/', views.deleteMedicamento, name='delete_medicamento'),
    path('cadastro_procedimento/', views.cadastro_procedimento, name='cadastro_procedimento'),
    path('update_procedimento/<int:pk>/', views.update_procedimento, name='update_procedimento'),
    path('delete_procedimento/<int:pk>/', views.deleteProcedimento, name='delete_procedimento'),
    #path('relatorio/', views.animal_relatorio, name='relatorio'),
    path('timeout/',  views.timeout_view, name='timeout'),
    path('api/', views.api_view, name='api'),
    path('estoque/adicionar/', views.adicionar_estoque, name='adicionar_estoque'),
    path('estoque/', views.listar_estoque, name='listar_estoque'),
    path('estoque/excluir/<int:estoque_id>/', views.excluir_estoque, name='excluir_estoque'),
    path('api/relatorio/pdf/<int:animal_id>/', RelatorioPDFAPIView.as_view(), name='api_relatorio_pdf'),







]