from django.shortcuts import render, get_object_or_404, redirect
from .models import Certificado
from django.http import HttpResponse
import re

# Create your views here.

def index(request):
    """
    Página inicial com formulário de pesquisa por CPF
    """
    certificados = []
    mensagem = None
    cpf_pesquisado = None

    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip()
        cpf_pesquisado = cpf

        # Limpa o CPF para busca (remove pontos, traços, etc)
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)

        if cpf_limpo:

            # Busca certificados pelo CPF - MODIFICADO para comparação exata
            certificados = []
            for cert in Certificado.objecs.all():

                # Limpa o CPF do banco para comparação
                cert_cpf_limpo = re.sub(r'[^0-9]', '', cert.cpf)
                if cert_cpf_limpo == cpf_limpo:
                    certificados.append(cert)

            if not certificados:
                mensagem = "Nenhum certificado encontrado para o CPF informado"
        else:
            mensagem = "Por favor, informe um CPF válido"

    return render(request, 'certificados/index.html', {
        'certificados': certificados,
        'mensagem': mensagem,
        'cpf_pesquisado': cpf_pesquisado
    })

def certificado_detalhe(request, codigo_validacao):
    """
    Exibe os detalhes de um certificado específico
    """
    certificado = get_object_or_404(Certificado, codigo_validacao=codigo_validacao)
    return render(request, 'certificados/certificado_detalhe.html', {
        'certificado': certificado
    })

def validar_certificado(request, codigo_validacao):
    """
    Página de validação do certificado via QR Code
    """
    certificado = get_object_or_404(Certificado, codigo_validacao)
    return render(request, 'certificados/validar_certificado.html', {
        'certificado': certificado,
        'validado': True
    })