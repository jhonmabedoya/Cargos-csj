from django.db import models
from django.conf import settings

class Novedad(models.Model):
    TIPOS_NOVEDAD = [
        ('renuncia', 'Renuncia'),
        ('provisionalidad', 'Provisionalidad'),
        ('propiedad', 'Propiedad'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPOS_NOVEDAD)
    cargo = models.ForeignKey('tipocargos.TipoCargo', on_delete=models.CASCADE)
    detalle = models.TextField()
    codigo_despacho = models.ForeignKey('despachos.Despacho', on_delete=models.CASCADE)
    nombre_despacho = models.CharField(max_length=200, editable=False)
    fecha_acto = models.DateField(verbose_name='Fecha de Acto Administrativo')
    fecha_posesion = models.DateField(verbose_name='Fecha de Posesión')
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_acto']
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'

    def __str__(self):
        return f"{self.get_tipo_display()} - ({self.fecha_acto})"

    def save(self, *args, **kwargs):
        if self.codigo_despacho:
            self.nombre_despacho = self.codigo_despacho.nombre
        super().save(*args, **kwargs)
