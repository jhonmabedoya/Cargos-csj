from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd
from core.decorators import requiere_magistrado
from .models import Funcionario
from .forms import FuncionarioForm
from .filters import FuncionarioFilter

@login_required
def lista(request):
    funcionario_filter = FuncionarioFilter(
        request.GET, 
        queryset=Funcionario.objects.all().order_by('nombre')
    )
    return render(request, 'funcionarios/lista.html', {
        'filter': funcionario_filter,
        'funcionarios': funcionario_filter.qs,
        'total_funcionarios': funcionario_filter.qs.count()
    })

@login_required
@requiere_magistrado
def crear(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funcionarios:lista')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/formulario.html', {
        'form': form,
        'titulo': 'Crear Nuevo Funcionario'
    })

@login_required
@requiere_magistrado
def editar(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('funcionarios:lista')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'funcionarios/formulario.html', {
        'form': form,
        'titulo': 'Editar Funcionario',
        'funcionario': funcionario
    })

@login_required
@requiere_magistrado
def eliminar(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('funcionarios:lista')
    return render(request, 'funcionarios/confirmar_eliminar.html', {
        'objeto': funcionario,
        'titulo': 'Eliminar Funcionario'
    })

@login_required
def exportar(request):
    funcionario_filter = FuncionarioFilter(request.GET, queryset=Funcionario.objects.all())
    funcionarios = funcionario_filter.qs.values(
        'nombre',
        'documento',
        'despacho__nombre',
        'cargo'
    )
    
    df = pd.DataFrame(funcionarios)
    df = df.rename(columns={
        'nombre': 'Nombre',
        'documento': 'Documento',
        'despacho__nombre': 'Despacho',
        'cargo': 'Cargo'
    })
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.xlsx"'
    
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Funcionarios')
        workbook = writer.book
        worksheet = writer.sheets['Funcionarios']
        
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
