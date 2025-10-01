from django.shortcuts import render

# Create your views here.
def tabelaAuditoria(request):
    return render(request, 'auditoria/tabela.html')