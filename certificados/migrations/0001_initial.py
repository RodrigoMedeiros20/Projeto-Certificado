# Generated by Django 5.2.1 on 2025-05-23 16:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_usuario', models.CharField(max_length=255, verbose_name='Nome do Usuário')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('nome_curso', models.CharField(max_length=255, verbose_name='Nome do Curso')),
                ('data_inicio', models.DateField(verbose_name='Data de Início')),
                ('data_final', models.DateField(verbose_name='Data de Conclusão')),
                ('codigo_validacao', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('data_emissao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Emissão')),
                ('qrcode_imagem', models.ImageField(blank=True, null=True, upload_to='qrcodes/')),
            ],
            options={
                'verbose_name': 'Certificado',
                'verbose_name_plural': 'Certificados',
                'indexes': [models.Index(fields=['cpf'], name='certificado_cpf_f186b1_idx'), models.Index(fields=['codigo_validacao'], name='certificado_codigo__b719d6_idx')],
            },
        ),
    ]
