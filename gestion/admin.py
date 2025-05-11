from django.contrib import admin

from .models import Paciente, Turno, Perfil


admin.site.register(Turno)

admin.site.register(Perfil)