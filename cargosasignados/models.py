from django.db import models
from despachos.models import Despacho
from tipocargos.models import TipoCargo
from django.conf import settings
# Create your models here.

class CargosAsignados(models.Model):
    OFERTABLE = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    
    despacho = models.ForeignKey(Despacho, on_delete=models.PROTECT)
    cargo = models.ForeignKey(TipoCargo, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    acuerdo = models.CharField(max_length=200)
    Ofertable = models.CharField(max_length=200, choices=OFERTABLE)
    estado_vacante = models.BooleanField(default=True)
    funcionario = models.ForeignKey('funcionarios.Funcionario', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    novedad = models.ForeignKey('novedades.Novedad', on_delete=models.SET_NULL, null=True, blank=True)
    # ... otros campos

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return f"{self.funcionario.nombre} - {self.cargo}"
