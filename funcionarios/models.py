from django.db import models
from despachos.models import Despacho
from tipocargos.models import TipoCargo

class Funcionario(models.Model):
    documento = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=200)
    despacho = models.ForeignKey(Despacho, on_delete=models.PROTECT)
    cargo = models.ForeignKey(TipoCargo, on_delete=models.PROTECT)
    escalafon = models.CharField(max_length=100, null=True, blank=True)
    genero = models.CharField(max_length=100, null=True, blank=True)
    convocatoria = models.CharField(max_length=100, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_ultima_novedad = models.DateField(null=True, blank=True)
    
    
    # ... otros campos

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
