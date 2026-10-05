from django import forms
from .models import Cliente, Veiculo, OrdemServico


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente

        fields = [
            'tipo',
            'nome',
            'cpf_cnpj',

            'rua',
            'numero',
            'bairro',
            'cep',
            'complemento',

            'cidade',
            'estado',

            'email',
            'telefone',
            'celular',
            'celular_secundario',

            'ativo',
        ]

class VeiculoForm(forms.ModelForm):

    class Meta:
        model = Veiculo

        fields = [
            'cliente',
            'tipo',
            'marca',
            'modelo',
            'ano',
            'cor',
            'placa',
            'combustivel',
            'ativo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].queryset = Cliente.objects.filter(
            ativo=True
        )
        
class OrdemServicoForm(forms.ModelForm):

    class Meta:
        model = OrdemServico

        fields = [
            'cliente',
            'veiculo',
            'solicitacao_cliente',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].queryset = Cliente.objects.filter(
            ativo=True
        )

        self.fields['veiculo'].queryset = Veiculo.objects.filter(
            ativo=True
        )

    def clean(self):
        cleaned_data = super().clean()

        cliente = cleaned_data.get('cliente')
        veiculo = cleaned_data.get('veiculo')

        if cliente and veiculo:

            if veiculo.cliente_id != cliente.id:
                self.add_error(
                    'veiculo',
                    'O veículo selecionado não pertence ao cliente informado.'
                )

            elif not veiculo.ativo:
                self.add_error(
                    'veiculo',
                    'O veículo selecionado está inativo.'
                )

        return cleaned_data