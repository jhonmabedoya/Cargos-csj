import django_filters
from django import forms
from django.db.models import Q
from .models import Novedad

class NovedadFilter(django_filters.FilterSet):
    busqueda = django_filters.CharFilter(
        method='filtro_busqueda',
        label='Búsqueda General',
        help_text='Buscar por funcionario u observaciones'
    )
    
    fecha_desde = django_filters.DateFilter(
        field_name='fecha_inicio',
        lookup_expr='gte',
        label='Fecha Desde',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    fecha_hasta = django_filters.DateFilter(
        field_name='fecha_fin',
        lookup_expr='lte',
        label='Fecha Hasta',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def filtro_busqueda(self, queryset, name, value):
        return queryset.filter(
            Q(funcionario__nombre__icontains=value) |
            Q(observaciones__icontains=value)
        )

    class Meta:
        model = Novedad
        fields = ['busqueda', 'tipo', 'fecha_desde', 'fecha_hasta'] 