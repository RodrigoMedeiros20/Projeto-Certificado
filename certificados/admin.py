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
        extra_context['title'] = "📄 Lista de Certificados"
        return super().changelist_view(request, extra_context)
    
    def importar_excel_view(self, request):
        if request.method == 'POST':
            excel_file = request.FILES.get('excel_file')

            if not excel_file:
                messages.error(request, 'Por favor, selecione um arquivo.')
                return redirect('..')

            filename = excel_file.name
            try:
                # Verifica extensão suportada
                if filename.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(excel_file)
                elif filename.endswith('.csv'):
                    df = pd.read_csv(excel_file)
                else:
                    messages.error(request, 'Formato inválido. Envie um arquivo .xlsx, .xls ou .csv.')
                    return redirect('..')

                # Colunas obrigatórias
                colunas_esperadas = ['Nome do usuário', 'CPF do usuário', 'Nome do curso',
                                    'Data início do curso', 'Data final do curso']

                # Validação de colunas exatas e na ordem correta
                if list(df.columns[:5]) != colunas_esperadas:
                    messages.error(request, f"As colunas estão incorretas ou fora de ordem. Esperado: {', '.join(colunas_esperadas)}.")
                    return redirect('..')

                certificados_importados = 0

                for _, row in df.iterrows():
                    try:
                        data_inicio = pd.to_datetime(row['Data início do curso']).date()
                        data_final = pd.to_datetime(row['Data final do curso']).date()

                        Certificado.objects.create(
                            nome_usuario=row['Nome do usuário'],
                            cpf=row['CPF do usuário'],
                            nome_curso=row['Nome do curso'],
                            data_inicio=data_inicio,
                            data_final=data_final
                        )
                        certificados_importados += 1
                    except Exception as e:
                        messages.warning(request, f'Erro ao importar linha: {e}')

                messages.success(request, f'{certificados_importados} certificados foram importados com sucesso.')
                return redirect('..')

            except Exception as e:
                messages.error(request, f'Erro ao processar o arquivo: {str(e)}')
                return redirect('..')

        return render(request, 'admin/importar_excel.html')


admin.site.register(Certificado, CertificadoAdmin)
