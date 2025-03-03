from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd
from core.decorators import requiere_magistrado
from .models import Novedad
from .forms import NovedadForm
from .filters import NovedadFilter

# Create your views here.

@login_required
def lista(request):
    novedad_filter = NovedadFilter(
        request.GET, 
        queryset=Novedad.objects.all().order_by('-fecha_inicio')
    )
    return render(request, 'novedades/lista.html', {
        'filter': novedad_filter,
        'novedades': novedad_filter.qs,
        'total_novedades': novedad_filter.qs.count()
    })

@login_required
@requiere_magistrado
def crear(request):
    if request.method == 'POST':
        form = NovedadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('novedades:lista')
    else:
        form = NovedadForm()
    return render(request, 'novedades/formulario.html', {
        'form': form,
        'titulo': 'Crear Nueva Novedad'
    })

@login_required
@requiere_magistrado
def editar(request, pk):
    novedad = get_object_or_404(Novedad, pk=pk)
    if request.method == 'POST':
        form = NovedadForm(request.POST, instance=novedad)
        if form.is_valid():
            form.save()
            return redirect('novedades:lista')
    else:
        form = NovedadForm(instance=novedad)
    return render(request, 'novedades/formulario.html', {
        'form': form,
        'titulo': 'Editar Novedad',
        'novedad': novedad
    })

@login_required
@requiere_magistrado
def eliminar(request, pk):
    novedad = get_object_or_404(Novedad, pk=pk)
    if request.method == 'POST':
        novedad.delete()
        return redirect('novedades:lista')
    return render(request, 'novedades/confirmar_eliminar.html', {
        'objeto': novedad,
        'titulo': 'Eliminar Novedad'
    })

@login_required
def exportar(request):
    novedad_filter = NovedadFilter(request.GET, queryset=Novedad.objects.all())
    novedades = novedad_filter.qs.values(
        'funcionario__nombre',
        'tipo',
        'fecha_inicio',
        'fecha_fin',
        'observaciones'
    )
    
    df = pd.DataFrame(novedades)
    df = df.rename(columns={
        'funcionario__nombre': 'Funcionario',
        'tipo': 'Tipo de Novedad',
        'fecha_inicio': 'Fecha Inicio',
        'fecha_fin': 'Fecha Fin',
        'observaciones': 'Observaciones'
    })
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="novedades.xlsx"'
    
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Novedades')
        workbook = writer.book
        worksheet = writer.sheets['Novedades']
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, len(value) + 5)
    
    return response
