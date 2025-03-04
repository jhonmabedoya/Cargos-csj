import django_filters
from django import forms
from django.db.models import Q
from django.apps import apps
from .models import Novedad

Novedad = apps.get_model('novedades', 'Novedad')

class NovedadFilter(django_filters.FilterSet):
    busqueda = django_filters.CharFilter(
        method='filtro_busqueda',
        label='Búsqueda General',
        help_text='Buscar en tipo, detalle o nombre del despacho'
    )
    
    fecha_desde = django_filters.DateFilter(
        field_name='fecha_acto',
        lookup_expr='gte',
        label='Fecha Desde',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    fecha_hasta = django_filters.DateFilter(
        field_name='fecha_acto',
        lookup_expr='lte',
        label='Fecha Hasta',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def filtro_busqueda(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(tipo__icontains=value) |
                Q(detalle__icontains=value) |
                Q(nombre_despacho__icontains=value)
            )
        return queryset

    class Meta:
        model = Novedad
        fields = ['tipo', 'codigo_despacho', 'fecha_acto', 'fecha_posesion'] 