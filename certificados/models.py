from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Certificado(models.Model):
    nome_usuario = models.CharField(max_length=255, verbose_name="Nome do Usuário")
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    nome_curso = models.CharField(max_length=255, verbose_name="Nome do Curso")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_final = models.DateField(verbose_name="Data de Conclusão")
    codigo_validacao = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data_emissao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Emissão")
    qrcode_imagem = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome_usuario} - {self.nome_curso}"
    
    def save(self, *args, **kwargs):
        # Gera um código de validação único se não existir
        if not self.codigo_validacao:
            self.codigo_validacao = uuid.uuid4()
            
        # Gera o QR Code apenas se o certificado já foi salvo (tem ID)
        if not self.qrcode_imagem and hasattr(self, 'id'):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # URL para validação do certificado
            qr_data = f"/validar/{self.codigo_validacao}/"
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            self.qrcode_imagem.save(f"qrcode-{self.codigo_validacao}.png", 
                                   File(buffer), save=False)
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        indexes = [
            models.Index(fields=['cpf']),
            models.Index(fields=['codigo_validacao']),
        ]
