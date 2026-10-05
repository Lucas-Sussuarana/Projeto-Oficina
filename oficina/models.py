from django.db import models, transaction


# ========================
# CLIENTE
# ========================
class Cliente(models.Model):

    TIPO_CLIENTE = [
        ('PESSOA', 'Pessoa Física'),
        ('EMPRESA', 'Empresa'),
    ]

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE,
        default='PESSOA'
    )

    nome = models.CharField(max_length=120)

    cpf_cnpj = models.CharField(
        max_length=20,
        unique=True
    )

    rua = models.CharField(max_length=120)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)
    complemento = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    email = models.EmailField()

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    celular = models.CharField(max_length=20)

    celular_secundario = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

# ========================
# VEICULO
# ========================

class Veiculo(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='veiculos'
    )

    tipo = models.CharField(max_length=50)

    marca = models.CharField(max_length=50)

    modelo = models.CharField(max_length=100)

    ano = models.CharField(max_length=10)

    cor = models.CharField(max_length=50)

    placa = models.CharField(max_length=10)

    combustivel = models.CharField(max_length=30)

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
# ========================
# PEÇA
# ========================
class Peca(models.Model):

    nome = models.CharField(max_length=120)

    descricao = models.TextField(
        blank=True,
        null=True
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estoque = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    estoque_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nome

# ========================
# SERVIÇO
# ========================
class Servico(models.Model):

    nome = models.CharField(max_length=120)

    descricao = models.TextField(
        blank=True,
        null=True
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    ativo = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nome

# ========================
# ORDEM DE SERVIÇO
# ========================
class OrdemServico(models.Model):

    STATUS_CHOICES = [
        ('ABERTA', 'Aberta'),
        ('EM_ATENDIMENTO', 'Em atendimento'),
        ('PRONTO', 'Pronto'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADA', 'Cancelada'),
    ]

    numero = models.PositiveIntegerField(
        unique=True,
        editable=False
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ordens_servico'
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name='ordens_servico'
    )

    solicitacao_cliente = models.TextField()

    motivo_cancelamento = models.TextField(
        blank=True,
        null=True
    )

    demanda_atendida = models.BooleanField(
        null=True,
        blank=True
    )

    motivo_nao_atendida = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ABERTA'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ABERTA'
    )

    observacao_final = models.TextField(
        blank=True,
        null=True
    )

    data_abertura = models.DateTimeField(
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    data_finalizacao = models.DateTimeField(
        blank=True,
        null=True
    )

    finalizado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='ordens_finalizadas',
        blank=True,
        null=True
    )

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo = OrdemServico.objects.order_by('-numero').first()

            if ultimo:
                self.numero = ultimo.numero + 1
            else:
                self.numero = 1

        super().save(*args, **kwargs)


    def calcular_total(self):
        total_servicos = sum(
            item.subtotal
            for item in self.itens_servico.all()
        )

        total_pecas = sum(
            item.subtotal
            for item in self.itens_peca.all()
        )

        self.valor_total = total_servicos + total_pecas
        self.save(update_fields=['valor_total'])

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.veiculo_id and self.cliente_id:
            if self.veiculo.cliente_id != self.cliente_id:
                raise ValidationError(
                    "O veículo selecionado não pertence ao cliente informado."
                )

    def __str__(self):
        return f"OS #{self.numero} - {self.veiculo}"
    

# ========================
# ITEM DE SERVIÇO DA OS
# ========================
class ItemServico(models.Model):

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='itens_servico'
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name='itens_ordem'
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0

    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.preco_unitario = self.servico.preco

        self.subtotal = self.quantidade * self.preco_unitario

        super().save(*args, **kwargs)

        self.ordem_servico.calcular_total()

    def __str__(self):
        return f"{self.servico.nome} - OS #{self.ordem_servico.id}"

# ========================
# ITEM DE PEÇA DA OS
# ========================
class ItemPeca(models.Model):

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='itens_peca'
    )

    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='itens_peca_oficina',
        blank=True,
        null=True
    )

    peca = models.ForeignKey(
        Peca,
        on_delete=models.PROTECT,
        related_name='itens_ordem'
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        novo_item = self._state.adding

        with transaction.atomic():

            if novo_item:
                self.preco_unitario = self.peca.preco
                self.subtotal = self.quantidade * self.preco_unitario

                super().save(*args, **kwargs)

                MovimentacaoEstoque.objects.create(
                    peca=self.peca,
                    tipo='SAIDA',
                    quantidade=self.quantidade,
                    ordem_servico=self.ordem_servico,
                    usuario=self.usuario
                )

            else:
                item_anterior = ItemPeca.objects.get(pk=self.pk)

                mudou_peca = (
                    item_anterior.peca_id != self.peca_id
                )

                diferenca = (
                    self.quantidade - item_anterior.quantidade
                )

                if mudou_peca:
                    # Devolve a peça antiga
                    MovimentacaoEstoque.objects.create(
                        peca=item_anterior.peca,
                        tipo='ENTRADA',
                        quantidade=item_anterior.quantidade,
                        ordem_servico=item_anterior.ordem_servico,
                        usuario=self.usuario
                    )

                    # Nova peça passa a usar o preço atual
                    self.preco_unitario = self.peca.preco
                    self.subtotal = (
                        self.quantidade * self.preco_unitario
                    )

                    super().save(*args, **kwargs)

                    # Retira a nova peça
                    MovimentacaoEstoque.objects.create(
                        peca=self.peca,
                        tipo='SAIDA',
                        quantidade=self.quantidade,
                        ordem_servico=self.ordem_servico,
                        usuario=self.usuario
                    )

                else:
                    self.subtotal = (
                        self.quantidade * self.preco_unitario
                    )

                    if diferenca > 0:
                        MovimentacaoEstoque.objects.create(
                            peca=self.peca,
                            tipo='SAIDA',
                            quantidade=diferenca,
                            ordem_servico=self.ordem_servico,
                            usuario=self.usuario
                        )

                    elif diferenca < 0:
                        MovimentacaoEstoque.objects.create(
                            peca=self.peca,
                            tipo='ENTRADA',
                            quantidade=abs(diferenca),
                            ordem_servico=self.ordem_servico,
                            usuario=self.usuario
                        )

                    super().save(*args, **kwargs)

            self.ordem_servico.calcular_total()

    def delete(self, *args, **kwargs):
        with transaction.atomic():

            MovimentacaoEstoque.objects.create(
                peca=self.peca,
                tipo='ENTRADA',
                quantidade=self.quantidade,
                ordem_servico=self.ordem_servico,
                usuario=self.usuario
            )

            ordem_servico = self.ordem_servico

            super().delete(*args, **kwargs)

            ordem_servico.calcular_total()

    def __str__(self):
        return f"{self.peca.nome} - OS #{self.ordem_servico.id}"

# ========================
# PARTICIPAÇÃO DO MECÂNICO
# ========================
class ParticipacaoMecanico(models.Model):

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='participacoes_mecanicos'
    )

    mecanico = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='participacoes_oficina'
    )

    data_entrada = models.DateTimeField(
        auto_now_add=True
    )

    data_saida = models.DateTimeField(
        blank=True,
        null=True
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.mecanico.username} - OS #{self.ordem_servico.id}"

# ========================
# OBSERVAÇÃO DA OS
# ========================
class Observacao(models.Model):

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='observacoes',
        blank=True,
        null=True
    )

    autor = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='observacoes_oficina',
        blank=True,
        null=True
    )

    texto = models.TextField()

    data = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Obs OS #{self.ordem_servico.id} - {self.autor.username}"

# ========================
# MOVIMENTAÇÃO DE ESTOQUE
# ========================
class MovimentacaoEstoque(models.Model):

    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]

    peca = models.ForeignKey(
        Peca,
        on_delete=models.PROTECT,
        related_name='movimentacoes_estoque'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.PROTECT,
        related_name='movimentacoes_estoque',
        blank=True,
        null=True
    )

    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='movimentacoes_estoque'
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        from django.db import transaction

        if not self._state.adding:
            super().save(*args, **kwargs)
            return

        with transaction.atomic():
            peca = Peca.objects.select_for_update().get(
                pk=self.peca_id
            )

            if self.tipo == 'SAIDA':
                if self.quantidade > peca.estoque:
                    raise ValidationError(
                        "Não há estoque suficiente para realizar esta saída."
                    )

                peca.estoque -= self.quantidade

            elif self.tipo == 'ENTRADA':
                peca.estoque += self.quantidade

            peca.save(update_fields=['estoque'])

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.peca.nome} - {self.quantidade}"