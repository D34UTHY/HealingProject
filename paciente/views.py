from django.shortcuts import render, redirect
from medico.models import DadosMedico, DatasAbertas, Especialidades, is_medico
from .models import Documento
from datetime import datetime
from .models import Consulta
from django.contrib import messages
from django.contrib.messages import constants

def home(request):
    if request.method == "GET":
        medicos = DadosMedico.objects.all()
        proxima_data = DatasAbertas.objects.filter(user=request.user).filter(data__gt=datetime.now()).filter(agendado=False).order_by('data').first()
        especialidades = Especialidades.objects.all()
        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.get('especialidades')

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains = medico_filtrar)
        
        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)
        
        return render(request, 'home.html', {'is_medico': is_medico(request.user)})
    
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})
    
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/pacientes/minhas_consultas/')
    
def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})

def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(id=consulta.data_aberta.user)
        return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico': dado_medico, 'id_medico': is_medico(request.user)})
    
def add_documento(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if consulta.data_aberta.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')

    if not documento:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

    documento = Documento(
        consulta=consulta,
        titulo=titulo,
        documento=documento

    )

    documento.save()

    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')    