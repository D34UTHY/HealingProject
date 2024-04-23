from django.contrib import admin
from .models import Especialidades, DadosMedico

# Register your models here.
admin.site.register(Especialidades) # Registra para levar o model ao site admnistrativo do django.
admin.site.register(DadosMedico) 