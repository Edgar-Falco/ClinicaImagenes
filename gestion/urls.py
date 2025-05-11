from django.urls import path
from . import views

urlpatterns = [
    # -------- Autenticación / Usuario --------
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),

    # -------- Paneles por Rol --------
    path('panel/paciente/', views.panel_paciente, name='panel_paciente'),
    path('panel/medico/', views.panel_medico, name='panel_medico'),
    path('panel/secretaria/', views.panel_secretaria, name='panel_secretaria'),

    # -------- Pacientes --------
    path('paciente/', views.registrar_paciente, name='registrar_paciente'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('buscar-paciente/', views.buscar_paciente, name='buscar_paciente'),
    path('mi_informe/', views.ver_informe, name='ver_informe'),

    # -------- Turnos --------
    path('turno/', views.registrar_turno, name='registrar_turno'),
    path('turnos/', views.lista_turnos, name='lista_turnos'),

    # -------- Informes --------
    path('cargar-informe/<int:paciente_id>/', views.cargar_informe, name='cargar_informe'),
    
    path('historia-clinica/<int:paciente_id>/', views.historia_clinica, name='historia_clinica'),
]
