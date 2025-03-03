import django_filters
from django.db.models import Q
from .models import Despacho

class DespachoFilter(django_filters.FilterSet):
    busqueda = django_filters.CharFilter(
        method='filtro_busqueda',
        label='Búsqueda General',
        help_text='Buscar en nombre, código o municipio'
    )
    
    jurisdiccion = django_filters.ChoiceFilter(
        choices=[
            ('ORDINARIA', 'Jurisdicción Ordinaria'),
            ('ADMINISTRATIVA', 'Jurisdicción Administrativa'),
            ('DISCIPLINARIA', 'Jurisdicción Disciplinaria'),
        ],
        label='Jurisdicción',
        empty_label='Todas las Jurisdicciones'
    )
    
    distrito = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Distrito'
    )
    
    circuito = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Circuito'
    )
    
    municipio = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Municipio'
    )

    def filtro_busqueda(self, queryset, name, value):
        return queryset.filter(
            Q(nombre__icontains=value) |
            Q(codigo__icontains=value) |
            Q(municipio__icontains=value)
        )

    class Meta:
        model = Despacho
        fields = ['busqueda', 'jurisdiccion', 'distrito', 'circuito', 'municipio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.form.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Buscar por {field.label}...'
            }) 