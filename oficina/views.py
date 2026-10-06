from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cliente, Veiculo, Servico, Peca, ItemServico, ItemPeca, Observacao, OrdemServico,  MovimentacaoEstoque,  ParticipacaoMecanico
from .forms import ClienteForm, VeiculoForm, OrdemServicoForm

@login_required
def home(request):
    return render(request, 'home.html')


# ========================
# CLIENTES
# ========================

# LISTAR
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def lista_clientes(request):
    clientes = Cliente.objects.all()

    return render(
        request,
        'clientes/lista_clientes.html',
        {'clientes': clientes}
    )


# CRIAR
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def criar_cliente(request):

    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_clientes')

    else:
        form = ClienteForm()

    return render(
        request,
        'clientes/form.html',
        {'form': form}
    )


# EDITAR
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('lista_clientes')

    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        'clientes/form.html',
        {'form': form}
    )


# EXCLUIR
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def excluir_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(
        request,
        'clientes/excluir.html',
        {'cliente': cliente}
    )

# ========================
# CRIAR VEICULO
# ========================
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def criar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_clientes')

    else:
        form = VeiculoForm()

    return render(
        request,
        'veiculos/form.html',
        {'form': form}
    )

# EDITAR VEICULO
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def editar_veiculo(request, id):

    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)

        if form.is_valid():
            form.save()
            return redirect('lista_clientes')

    else:
        form = VeiculoForm(instance=veiculo)

    return render(
        request,
        'veiculos/form.html',
        {'form': form}
    )

# EXCLUIR VEICULO
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def excluir_veiculo(request, id):

    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == 'POST':
        veiculo.delete()
        return redirect('lista_clientes')

    return render(
        request,
        'veiculos/excluir.html',
        {'veiculo': veiculo}
    )

# ========================
# SERVIÇOS
# ========================

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def criar_servico(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')

        if nome and preco:
            Servico.objects.create(
                nome=nome,
                descricao=descricao,
                preco=preco
            )

            return redirect('lista_clientes')

    return render(
        request,
        'servicos/form.html'
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def lista_servicos(request):

    servicos = Servico.objects.all().order_by('nome')

    return render(
        request,
        'servicos/lista.html',
        {'servicos': servicos}
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def editar_servico(request, id):

    servico = get_object_or_404(Servico, id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        ativo = request.POST.get('ativo')

        if nome and preco:
            servico.nome = nome
            servico.descricao = descricao
            servico.preco = preco
            servico.ativo = ativo == 'on'
            servico.save()

            return redirect('lista_servicos')

    return render(
        request,
        'servicos/form.html',
        {'servico': servico}
    )

# ========================
# PEÇAS
# ========================

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def criar_peca(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        estoque_minimo = request.POST.get('estoque_minimo')

        if nome and preco and estoque_minimo:
            Peca.objects.create(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque_minimo=estoque_minimo
            )

            return redirect('lista_pecas')

    return render(
        request,
        'pecas/form.html'
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def lista_pecas(request):

    pecas = Peca.objects.all().order_by('nome')

    return render(
        request,
        'pecas/lista.html',
        {'pecas': pecas}
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def editar_peca(request, id):

    peca = get_object_or_404(Peca, id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        estoque_minimo = request.POST.get('estoque_minimo')
        ativo = request.POST.get('ativo')

        if nome and preco and estoque_minimo:
            peca.nome = nome
            peca.descricao = descricao
            peca.preco = preco
            peca.estoque_minimo = estoque_minimo
            peca.ativo = ativo == 'on'
            peca.save()

            return redirect('lista_pecas')

    return render(
        request,
        'pecas/form.html',
        {'peca': peca}
    )

# ========================
# ENTRADA DE ESTOQUE
# ========================

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def entrada_estoque(request, id):

    peca = get_object_or_404(
        Peca,
        id=id,
        ativo=True
    )

    if request.method == 'POST':
        from decimal import Decimal

        quantidade = request.POST.get('quantidade')
        observacao = request.POST.get('observacao')

        if quantidade:
            quantidade = Decimal(quantidade)

            MovimentacaoEstoque.objects.create(
                peca=peca,
                tipo='ENTRADA',
                quantidade=quantidade,
                usuario=request.user,
                observacao=observacao
            )

            return redirect('lista_pecas')

    return render(
        request,
        'pecas/entrada_estoque.html',
        {'peca': peca}
    )

# ========================
# ORDENS DE SERVIÇO
# ========================
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def abrir_ordem_servico(request):

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)

        if form.is_valid():
            ordem = form.save()

            return redirect(
                'ordem_servico_criada',
                numero=ordem.numero
            )

    else:
        form = OrdemServicoForm()

    return render(
        request,
        'oficina/abrir_ordem_servico.html',
        {'form': form}
    )


def ordem_servico_criada(request, numero):

    return render(
        request,
        'oficina/ordem_servico_criada.html',
        {'numero': numero}
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def veiculos_por_cliente(request):
    cliente_id = request.GET.get('cliente_id')

    if not cliente_id:
        return render(
            request,
            'oficina/veiculos_options.html',
            {'veiculos': []}
        )

    veiculos = Veiculo.objects.filter(
        cliente_id=cliente_id,
        ativo=True
    ).order_by('modelo')

    return render(
        request,
        'oficina/veiculos_options.html',
        {'veiculos': veiculos}
    )


@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter( name__in=['Mecânicos', 'Recepcionistas'] ).exists()
)
def lista_ordens_servico(request):

    ordens = OrdemServico.objects.filter(
        status__in=['ABERTA', 'EM_ATENDIMENTO']
    ).select_related(
        'cliente',
        'veiculo'
    ).order_by(
        'data_abertura'
    )

    return render(
        request,
        'oficina/lista_ordens_servico.html',
        {'ordens': ordens}
    )

@user_passes_test(
    lambda user: (
        user.is_superuser
        or user.groups.filter(
            name__in=['Mecânicos', 'Recepcionistas']
        ).exists()
    )
)

@user_passes_test(
    lambda user:  user.is_superuser or user.groups.filter(name='Recepcionistas').exists()
)
def lista_ordens_prontas(request):

    ordens = OrdemServico.objects.filter(
        status='PRONTO'
    ).select_related(
        'cliente',
        'veiculo',
        'finalizado_por'
    ).order_by(
        '-data_finalizacao'
    )

    return render(
        request,
        'oficina/lista_ordens_prontas.html',
        {'ordens': ordens}
    )

@login_required
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists()  
)
def lista_ordens_entregues(request):

    ordens = OrdemServico.objects.filter(
        status='ENTREGUE'
    ).select_related(
        'cliente',
        'veiculo',
        'finalizado_por'
    ).order_by(
        '-data_finalizacao'
    )

    return render(
        request,
        'oficina/lista_ordens_entregues.html',
        {'ordens': ordens}
    )

@login_required
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
def lista_ordens_mecanico(request):
    ordens = OrdemServico.objects.filter(
        status__in=['ABERTA', 'EM_ATENDIMENTO']
    ).select_related(
        'cliente',
        'veiculo'
    ).prefetch_related(
        'participacoes_mecanicos__mecanico'
    ).order_by('data_abertura')

    return render(
        request,
        'oficina/lista_ordens_mecanico.html',
        {'ordens': ordens}
    )

def detalhe_ordem_servico(request, numero):

    ordem = get_object_or_404(
        OrdemServico.objects.select_related(
            'cliente',
            'veiculo'
        ),
        numero=numero
    )

    servicos = Servico.objects.filter(
        ativo=True
    ).order_by('nome')

    pecas = Peca.objects.filter(
        ativo=True
    ).order_by('nome')

    participacao_aberta = ParticipacaoMecanico.objects.filter(
        ordem_servico=ordem,
        mecanico=request.user,
        data_saida__isnull=True
    ).exists()

    return render(
        request,
        'oficina/detalhe_ordem_servico.html',
        {
            'ordem': ordem,
            'servicos': servicos,
            'pecas': pecas,
            'participacao_aberta': participacao_aberta,
        }
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
def iniciar_atendimento(request, numero):

    ordem = get_object_or_404(
        OrdemServico,
        numero=numero
    )

    if request.method == 'POST':

        participacao_existente = ParticipacaoMecanico.objects.filter(
            ordem_servico=ordem,
            mecanico=request.user,
            data_saida__isnull=True
        ).exists()

        if not participacao_existente:

            ParticipacaoMecanico.objects.create(
                ordem_servico=ordem,
                mecanico=request.user
            )

        if ordem.status == 'ABERTA':
            ordem.status = 'EM_ATENDIMENTO'
            ordem.save()

        return redirect(
            'detalhe_ordem_servico',
            numero=ordem.numero
        )

    return redirect(
        'detalhe_ordem_servico',
        numero=ordem.numero
    )
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
def adicionar_servico(request, numero):

    ordem = get_object_or_404(
        OrdemServico,
        numero=numero
    )

    if request.method == 'POST':

        servico_id = request.POST.get('servico')
        quantidade = request.POST.get('quantidade', 1)

        servico = get_object_or_404(
            Servico,
            id=servico_id,
            ativo=True
        )

        from decimal import Decimal

        quantidade = Decimal(quantidade)

        ItemServico.objects.create(
            ordem_servico=ordem,
            servico=servico,
            quantidade=quantidade
        )

        return redirect(
            'detalhe_ordem_servico',
            numero=ordem.numero
        )

    return redirect(
        'detalhe_ordem_servico',
        numero=ordem.numero
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
def adicionar_peca(request, numero):

    ordem = get_object_or_404(
        OrdemServico,
        numero=numero
    )

    if request.method == 'POST':

        peca_id = request.POST.get('peca')
        quantidade = request.POST.get('quantidade', 1)

        peca = get_object_or_404(
            Peca,
            id=peca_id,
            ativo=True
        )

        from decimal import Decimal

        quantidade = Decimal(quantidade)

        ItemPeca.objects.create(
            ordem_servico=ordem,
            peca=peca,
            quantidade=quantidade,
            usuario=request.user
        )

        return redirect(
            'detalhe_ordem_servico',
            numero=ordem.numero
        )

    return redirect(
        'detalhe_ordem_servico',
        numero=ordem.numero
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
def adicionar_observacao(request, numero):

    ordem = get_object_or_404(
        OrdemServico,
        numero=numero
    )

    if request.method == 'POST':

        texto = request.POST.get('texto')

        if texto:
            Observacao.objects.create(
                ordem_servico=ordem,
                autor=request.user,
                texto=texto
            )

        return redirect(
            'detalhe_ordem_servico',
            numero=ordem.numero
        )

    return redirect(
        'detalhe_ordem_servico',
        numero=ordem.numero
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Mecânicos').exists()
)
def finalizar_ordem_servico(request, numero):

    ordem = get_object_or_404(
        OrdemServico,
        numero=numero
    )

    if request.method == 'POST':

        demanda_atendida = request.POST.get(
            'demanda_atendida'
        )

        motivo_nao_atendida = request.POST.get(
            'motivo_nao_atendida'
        )

        observacao_final = request.POST.get(
            'observacao_final'
        )

        if demanda_atendida == 'SIM':
            ordem.demanda_atendida = True
            ordem.motivo_nao_atendida = None

        elif demanda_atendida == 'NAO':
            ordem.demanda_atendida = False
            ordem.motivo_nao_atendida = motivo_nao_atendida

        ordem.observacao_final = observacao_final
        ordem.status = 'PRONTO'
        ordem.finalizado_por = request.user

        from django.utils import timezone

        ordem.data_finalizacao = timezone.now()

        ordem.data_finalizacao = timezone.now()

        data_saida = ordem.data_finalizacao

        ParticipacaoMecanico.objects.filter(
            ordem_servico=ordem,
            data_saida__isnull=True
        ).update(
            data_saida=data_saida
        )

        ordem.save()

        return redirect(
            'detalhe_ordem_servico',
            numero=ordem.numero
        )

    return redirect(
        'detalhe_ordem_servico',
        numero=ordem.numero
    )

@user_passes_test(
    lambda user: user.is_superuser or user.groups.filter(name='Recepcionistas').exists(),

)
def entregar_ordem_servico(request, numero):

    ordem = get_object_or_404(
        OrdemServico,
        numero=numero
    )

    if request.method == 'POST':

        if ordem.status == 'PRONTO':
            ordem.status = 'ENTREGUE'
            ordem.save()

        return redirect(
            'detalhe_ordem_servico',
            numero=ordem.numero
        )

    return redirect(
        'detalhe_ordem_servico',
        numero=ordem.numero
    )