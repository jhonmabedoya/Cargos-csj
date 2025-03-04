from django.db import models

# Create your models here.
class TipoCargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Tipo de Cargo'
        verbose_name_plural = 'Tipos de Cargos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre