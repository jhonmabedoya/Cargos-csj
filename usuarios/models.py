from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('magistrado', 'Magistrado'),
        ('secretario', 'Secretario'),
        ('auxiliar', 'Auxiliar'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO,
        default='auxiliar'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios' 