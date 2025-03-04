from django.db import models

# Create your models here.

class Despacho(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    jurisdiccion = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    circuito = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['jurisdiccion', 'distrito', 'circuito']
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
