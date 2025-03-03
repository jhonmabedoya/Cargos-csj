from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd
from core.decorators import requiere_magistrado
from .models import Despacho
from .forms import DespachoForm
from .filters import DespachoFilter

# Create your views here.

@login_required
def lista(request):
    despacho_filter = DespachoFilter(
        request.GET, 
        queryset=Despacho.objects.all().order_by('jurisdiccion', 'distrito', 'circuito')
    )
    return render(request, 'despachos/lista.html', {
        'filter': despacho_filter,
        'despachos': despacho_filter.qs,
        'total_despachos': despacho_filter.qs.count()
    })

@login_required
@requiere_magistrado
def crear(request):
    if request.method == 'POST':
        form = DespachoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('despachos:lista')
    else:
        form = DespachoForm()
    return render(request, 'despachos/formulario.html', {
        'form': form,
        'titulo': 'Crear Nuevo Despacho'
    })

@login_required
@requiere_magistrado
def editar(request, pk):
    despacho = get_object_or_404(Despacho, pk=pk)
    if request.method == 'POST':
        form = DespachoForm(request.POST, instance=despacho)
        if form.is_valid():
            form.save()
            return redirect('despachos:lista')
    else:
        form = DespachoForm(instance=despacho)
    return render(request, 'despachos/formulario.html', {
        'form': form,
        'titulo': 'Editar Despacho',
        'despacho': despacho
    })

@login_required
@requiere_magistrado
def eliminar(request, pk):
    despacho = get_object_or_404(Despacho, pk=pk)
    if request.method == 'POST':
        despacho.delete()
        return redirect('despachos:lista')
    return render(request, 'despachos/confirmar_eliminar.html', {
        'objeto': despacho,
        'titulo': 'Eliminar Despacho'
    })

@login_required
def exportar(request):
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

# ... otras vistas
