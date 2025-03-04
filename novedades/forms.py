from django import forms
from django.apps import apps

class NovedadForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('novedades', 'Novedad')
        fields = ['tipo',  'detalle', 'codigo_despacho', 'fecha_acto', 'fecha_posesion', 'observaciones']
        widgets = {
            'fecha_acto': forms.DateInput(attrs={'type': 'date'}),
            'fecha_posesion': forms.DateInput(attrs={'type': 'date'}),
            'detalle': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_acto'].widget.attrs.update({'type': 'date'})
        self.fields['fecha_posesion'].widget.attrs.update({'type': 'date'}) 