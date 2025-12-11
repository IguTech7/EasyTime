from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def listar_funcionarios(request):
    return render(request, 'funcionarios/listar.html')
