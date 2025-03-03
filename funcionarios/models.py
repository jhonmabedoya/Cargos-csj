from django.db import models
from despachos.models import Despacho

class Funcionario(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=20, unique=True)
    despacho = models.ForeignKey(Despacho, on_delete=models.PROTECT)
    cargo = models.CharField(max_length=100)
    # ... otros campos

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
