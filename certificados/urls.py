from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('certificado/<uuid:codigo_validacao>/', views.certificado_detalhe, name='certificado_detalhe'),
    path('validar/<uuid:codigo_validacao>/', views.validar_certificado, name='validar_certificado'),
]
