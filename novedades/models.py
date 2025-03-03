from django.db import models
from funcionarios.models import Funcionario

class Novedad(models.Model):
    TIPOS_NOVEDAD = [
        ('LICENCIA', 'Licencia'),
        ('VACACIONES', 'Vacaciones'),
        ('PERMISO', 'Permiso'),
        # ... otros tipos
    ]
    
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=20, choices=TIPOS_NOVEDAD)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'

    def __str__(self):
        return f"{self.funcionario} - {self.tipo} ({self.fecha_inicio})"
