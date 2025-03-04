from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.apps import apps
from .forms import NovedadForm
from .filters import NovedadFilter
import pandas as pd
from datetime import datetime

# Create your views here.

Novedad = apps.get_model('novedades', 'Novedad')

@login_required
def lista(request):
    novedades = Novedad.objects.all()
    filtro = NovedadFilter(request.GET, queryset=novedades)
    novedades = filtro.qs
    return render(request, 'novedades/lista.html', {
        'novedades': novedades,
        'filtro': filtro
    })

@login_required
def crear(request):
    if request.method == 'POST':
        form = NovedadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novedad creada exitosamente.')
            return redirect('novedades:lista')
    else:
        form = NovedadForm()
    return render(request, 'novedades/formulario.html', {
        'form': form,
        'titulo': 'Nueva Novedad'
    })

@login_required
def editar(request, pk):
    novedad = get_object_or_404(Novedad, pk=pk)
    if request.method == 'POST':
        form = NovedadForm(request.POST, instance=novedad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novedad actualizada exitosamente.')
            return redirect('novedades:lista')
    else:
        form = NovedadForm(instance=novedad)
    return render(request, 'novedades/formulario.html', {
        'form': form,
        'titulo': 'Editar Novedad'
    })

@login_required
def eliminar(request, pk):
    novedad = get_object_or_404(Novedad, pk=pk)
    if request.method == 'POST':
        novedad.delete()
        messages.success(request, 'Novedad eliminada exitosamente.')
        return redirect('novedades:lista')
    return render(request, 'novedades/confirmar_eliminar.html', {
        'novedad': novedad
    })

@login_required
def exportar(request):
    novedades = Novedad.objects.all()
    filtro = NovedadFilter(request.GET, queryset=novedades)
    novedades = filtro.qs

    # Crear DataFrame
    data = []
    for novedad in novedades:
        data.append({
            'Tipo': novedad.get_tipo_display(),
            'Cargo': str(novedad.cargo),
            'Detalle': novedad.detalle,
            'Despacho': novedad.nombre_despacho,
            'Fecha Acto': novedad.fecha_acto.strftime('%d/%m/%Y'),
            'Fecha Posesión': novedad.fecha_posesion.strftime('%d/%m/%Y'),
            'Observaciones': novedad.observaciones or ''
        })

    df = pd.DataFrame(data)

    # Crear archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="novedades_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Novedades', index=False)
        
        # Obtener el objeto workbook y worksheet
        workbook = writer.book
        worksheet = writer.sheets['Novedades']
        
        # Formato para los encabezados
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4B5563',
            'font_color': 'white',
            'border': 1
        })
        
        # Aplicar formato a los encabezados
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Ajustar el ancho de las columnas
        for idx, col in enumerate(df):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(str(col))
            )
            worksheet.set_column(idx, idx, max_length + 2)

    return response
