from django import forms
from .models import Novedad

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['funcionario', 'tipo', 'fecha_inicio', 'fecha_fin', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        } 