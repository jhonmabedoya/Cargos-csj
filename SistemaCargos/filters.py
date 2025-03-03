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
        label='Distrito',
        help_text='Ingrese el nombre del distrito'
    )
    
    circuito = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Circuito',
        help_text='Ingrese el nombre del circuito'
    )
    
    municipio = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Municipio',
        help_text='Ingrese el nombre del municipio'
    )

    def filtro_busqueda(self, queryset, name, value):
        """
        Método para realizar búsqueda en múltiples campos
        """
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
        # Personalizar los widgets de los campos
        for field in self.form.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Buscar por {field.label}...'
            })