from django import forms
from .models import Despacho

class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = ['jurisdiccion', 'distrito', 'circuito', 'municipio', 'codigo', 'nombre', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        } 