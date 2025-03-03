import django_filters
from django.db.models import Q
from .models import Funcionario

class FuncionarioFilter(django_filters.FilterSet):
    busqueda = django_filters.CharFilter(
        method='filtro_busqueda',
        label='Búsqueda General',
        help_text='Buscar por nombre, documento o cargo'
    )
    
    despacho = django_filters.CharFilter(
        field_name='despacho__nombre',
        lookup_expr='icontains',
        label='Despacho'
    )

    def filtro_busqueda(self, queryset, name, value):
        return queryset.filter(
            Q(nombre__icontains=value) |
            Q(documento__icontains=value) |
            Q(cargo__icontains=value)
        )

    class Meta:
        model = Funcionario
        fields = ['busqueda', 'despacho'] 