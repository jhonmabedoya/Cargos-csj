from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from despachos.models import Despacho
from funcionarios.models import Funcionario
from novedades.models import Novedad

# Create your views here.

@login_required
def dashboard(request):
    context = {
        'total_despachos': Despacho.objects.count(),
        'total_funcionarios': Funcionario.objects.count(),
        'total_novedades': Novedad.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)
