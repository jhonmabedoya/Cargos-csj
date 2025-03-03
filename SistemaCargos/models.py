# Definir modelos en cargos/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('INV', 'Invitado'),
        ('MAG', 'Magistrado'),
    ]
    tipo_usuario = models.CharField(max_length=3, choices=TIPO_USUARIO, default='INV')
    
    # Modificar las relaciones para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Despacho(models.Model):
    jurisdiccion = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    circuito = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Novedad(models.Model):
    TIPO_NOVEDAD = [
        ('PROV', 'Provisionalidad'),
        ('PROP', 'Propiedad'),
        ('REN', 'Renuncia'),
    ]
    despacho = models.ForeignKey(Despacho, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=4, choices=TIPO_NOVEDAD)
    fecha = models.DateField(auto_now_add=True)
    detalle = models.TextField()

    def __str__(self):
        return f'{self.despacho.nombre} - {self.get_tipo_display()}'

class Funcionario(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    despacho = models.ForeignKey(Despacho, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre