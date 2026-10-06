from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),

    path('', views.home, name='home'),

    # CLIENTES
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

    # ORDENS DE SERVIÇO
    path(
        'ordens/abrir/',
        views.abrir_ordem_servico,
        name='abrir_ordem_servico'
    ),

    path(
        'ordens/criada/<int:numero>/',
        views.ordem_servico_criada,
        name='ordem_servico_criada'
    ),

    path(
        'veiculos-por-cliente/',
        views.veiculos_por_cliente,
        name='veiculos_por_cliente'
    ),

    path(
        'ordens/',
        views.lista_ordens_servico,
        name='lista_ordens_servico'
    ),

    path(
        'ordens/<int:numero>/',
        views.detalhe_ordem_servico,
        name='detalhe_ordem_servico'
    ),

    path(
        'ordens/<int:numero>/iniciar/',
        views.iniciar_atendimento,
        name='iniciar_atendimento'
    ),

    path(
        'ordens/<int:numero>/adicionar-servico/',
        views.adicionar_servico,
        name='adicionar_servico'
    ),

    path(
        'ordens/<int:numero>/adicionar-peca/',
        views.adicionar_peca,
        name='adicionar_peca'
    ),

    path(
        'ordens/<int:numero>/adicionar-observacao/',
        views.adicionar_observacao,
        name='adicionar_observacao'
    ),

    path(
        'ordens/<int:numero>/finalizar/',
        views.finalizar_ordem_servico,
        name='finalizar_ordem_servico'
    ),    

    path(
        'ordens/<int:numero>/entregar/',
        views.entregar_ordem_servico,
        name='entregar_ordem_servico'
    ),

    path(
        'veiculos/novo/',
        views.criar_veiculo,
        name='criar_veiculo'
    ),

    path(
        'veiculos/editar/<int:id>/',
        views.editar_veiculo,
        name='editar_veiculo'
    ),

    path(
        'veiculos/excluir/<int:id>/',
        views.excluir_veiculo,
        name='excluir_veiculo'
    ),

    path(
        'servicos/novo/',
        views.criar_servico,
        name='criar_servico'
    ),

    path(
        'servicos/',
        views.lista_servicos,
        name='lista_servicos'
    ),

    path(
        'servicos/editar/<int:id>/',
        views.editar_servico,
        name='editar_servico'
    ),

    path(
        'pecas/novo/',
        views.criar_peca,
        name='criar_peca'
    ),

    path(
        'pecas/',
        views.lista_pecas,
        name='lista_pecas'
    ),

    path(
        'pecas/editar/<int:id>/',
        views.editar_peca,
        name='editar_peca'
    ),

]