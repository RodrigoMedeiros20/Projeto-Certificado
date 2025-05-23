from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Certificado
import pandas as pd
from datetime import datetime

class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'cpf', 'nome_curso', 'data_inicio', 'data_final', 'data_emissao')
    search_fields = ('nome_usuario', 'cpf', 'nome_curso')
    list_filter = ('data_emissao', 'data_final')
    readonly_fields = ('codigo_validacao', 'data_emissao', 'qrcode_imagem')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('importar-excel/', self.admin_site.admin_view(self.importar_excel_view), name='importar_excel'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context)
    
    def importar_excel_view(self, request):
        if request.method == 'POST':
            excel_file = request.FILES.get('excel_file')
            if excel_file and excel_file.name.endswith(('.xlsx', '.xls')):
                try:
                    # Lê o arquivo Excel
                    df = pd.read_excel(excel_file)
                    
                    # Verifica se todas as colunas necessárias estão presentes
                    colunas_necessarias = ['Nome do usuário', 'CPF do usuário', 'Nome do curso', 
                                          'Data início do curso', 'Data final do curso']
                    
                    # Verifica se todas as colunas necessárias estão presentes
                    if not all(coluna in df.columns for coluna in colunas_necessarias):
                        messages.error(request, 'O arquivo Excel não contém todas as colunas necessárias.')
                        return redirect('..')
                    
                    # Contador de certificados importados
                    certificados_importados = 0
                    
                    # Processa cada linha do Excel
                    for _, row in df.iterrows():
                        try:
                            # Converte as datas para o formato correto
                            data_inicio = pd.to_datetime(row['Data início do curso']).date()
                            data_final = pd.to_datetime(row['Data final do curso']).date()
                            
                            # Cria ou atualiza o certificado
                            Certificado.objects.create(
                                nome_usuario=row['Nome do usuário'],
                                cpf=row['CPF do usuário'],
                                nome_curso=row['Nome do curso'],
                                data_inicio=data_inicio,
                                data_final=data_final
                            )
                            certificados_importados += 1
                        except Exception as e:
                            messages.warning(request, f'Erro ao processar linha: {e}')
                    
                    messages.success(request, f'{certificados_importados} certificados foram importados com sucesso!')
                    return redirect('..')
                except Exception as e:
                    messages.error(request, f'Erro ao processar o arquivo Excel: {e}')
                    return redirect('..')
            else:
                messages.error(request, 'Por favor, envie um arquivo Excel válido (.xlsx ou .xls).')
                return redirect('..')
        
        # Se for GET, exibe o formulário de upload
        return render(request, 'admin/importar_excel.html')

admin.site.register(Certificado, CertificadoAdmin)
