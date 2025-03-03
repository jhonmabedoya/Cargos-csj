# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Despacho, Novedad, Funcionario
from django.http import HttpResponse
import pandas as pd
from .filters import DespachoFilter
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm

#dashboard
@login_required
def dashboard(request):
    return render(request, 'cargos/dashboard.html', {'user': request.user})

def es_magistrado(user):
    return user.tipo_usuario == 'MAG'

def requiere_magistrado(view_func):
    def check_magistrado(request, *args, **kwargs):
        if not request.user.is_authenticated or not es_magistrado(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return check_magistrado

# Primero, definimos el formulario
class DespachoForm(ModelForm):
    class Meta:
        model = Despacho
        fields = ['jurisdiccion', 'distrito', 'circuito', 'municipio', 'codigo', 'nombre', 'observaciones']

@login_required
@requiere_magistrado  # Aseguramos que solo los magistrados puedan crear/editar
def crear_despacho(request):
    if request.method == 'POST':
        form = DespachoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_despachos')
    else:
        form = DespachoForm()
    return render(request, 'cargos/formulario.html', {
        'form': form,
        'titulo': 'Crear Nuevo Despacho'
    })

@login_required
def listar_despachos(request):
    despachos = Despacho.objects.all()
    return render(request, 'cargos/despachos.html', {'despachos': despachos})

#listar novedades
@login_required
def listar_novedades(request):
    novedades = Novedad.objects.all()
    return render(request, 'cargos/novedades.html', {'novedades': novedades})

#listar funcionarios
@login_required
def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'cargos/funcionarios.html', {'funcionarios': funcionarios})

#listar y filtrar despachos
@login_required
def listar_despachos(request):
    filtro = DespachoFilter(request.GET, queryset=Despacho.objects.all())
    return render(request, 'cargos/despachos.html', {'filter': filtro})

#exportar datos a excel
@login_required
def exportar_despachos(request):
    # Obtener el filtro actual
    despacho_filter = DespachoFilter(request.GET, queryset=Despacho.objects.all())
    # Exportar solo los despachos filtrados
    despachos = despacho_filter.qs.values(
        'codigo', 
        'nombre', 
        'jurisdiccion', 
        'distrito', 
        'circuito', 
        'municipio',
        'observaciones'
    )
    
    df = pd.DataFrame(despachos)
    
    # Renombrar columnas para mejor presentación
    df = df.rename(columns={
        'codigo': 'Código',
        'nombre': 'Nombre',
        'jurisdiccion': 'Jurisdicción',
        'distrito': 'Distrito',
        'circuito': 'Circuito',
        'municipio': 'Municipio',
        'observaciones': 'Observaciones'
    })
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="despachos.xlsx"'
    
    # Exportar a Excel con formato
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Despachos')
        
        # Obtener el objeto workbook y worksheet
        workbook = writer.book
        worksheet = writer.sheets['Despachos']
        
        # Formato para los encabezados
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1
        })
        
        # Aplicar formato a los encabezados
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, len(value) + 5)
    
    return response

#crear funcionario

@login_required
@user_passes_test(es_magistrado)
def crear_funcionario(request):
    return render(request, 'cargos/crear_funcionario.html')

@login_required
@requiere_magistrado
def editar_despacho(request, pk):
    despacho = get_object_or_404(Despacho, pk=pk)
    if request.method == 'POST':
        form = DespachoForm(request.POST, instance=despacho)
        if form.is_valid():
            form.save()
            return redirect('listar_despachos')
    else:
        form = DespachoForm(instance=despacho)
    return render(request, 'cargos/formulario.html', {
        'form': form,
        'titulo': 'Editar Despacho',
        'despacho': despacho
    })

@login_required
@requiere_magistrado
def eliminar_despacho(request, pk):
    despacho = get_object_or_404(Despacho, pk=pk)
    if request.method == 'POST':
        despacho.delete()
        return redirect('listar_despachos')
    return render(request, 'cargos/confirmar_eliminar.html', {
        'objeto': despacho,
        'titulo': 'Eliminar Despacho'
    })