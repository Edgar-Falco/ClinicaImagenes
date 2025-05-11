from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import (
    PacienteForm, TurnoForm, RegistroUsuarioForm,
    InformeForm
)
from .models import Paciente, Turno, Perfil, Informe
from .decoradores import rol_requerido



from .decoradores import rol_requerido  # Si usás esto para control por rol

from .forms import RegistroForm





### ========== 1. LOGIN / LOGOUT / REGISTRO ==========
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'gestion/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Crear perfil vinculado
            Perfil.objects.create(user=user, rol=form.cleaned_data['rol'])
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'gestion/registro.html', {'form': form})


### ========== 2. INICIO CON REDIRECCIÓN POR ROL ==========
@login_required
def inicio(request):
    try:
        rol = request.user.perfil.rol
    except Perfil.DoesNotExist:
        return redirect('no_autorizado')

    if rol == 'paciente':
        return redirect('panel_paciente')
    elif rol == 'medico':
        return redirect('panel_medico')
    elif rol == 'secretaria':
        return redirect('panel_secretaria')
    else:
        return redirect('no_autorizado')


### ========== 3. VISTAS PARA CADA ROL ==========

# --- SECRETARIA ---
@login_required
@rol_requerido(['secretaria'])  # Solo la secretaria puede registrar pacientes
def registrar_paciente(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # si usás 2 campos de password
            user.save()

            # Crear el perfil del usuario con rol 'paciente'
            Perfil.objects.create(user=user, rol='paciente')

            # Crear perfil de paciente asociado
            Paciente.objects.create(
                user=user,
                nombre=user.first_name,
                apellido=user.last_name,
                dni=form.cleaned_data['dni'],
                fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento'),
                email=user.email,
            )

            return redirect('lista_pacientes')
    else:
        form = RegistroForm()
    
    return render(request, 'gestion/registrar_paciente.html', {'form': form})




@login_required
@rol_requerido(['secretaria'])
def registrar_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_turno')
    else:
        form = TurnoForm()
    return render(request, 'gestion/registrar_turno.html', {'form': form})


@login_required
@rol_requerido(['secretaria'])
def panel_secretaria(request):
    return render(request, 'gestion/panel_secretaria.html')


# --- MÉDICO ---

@login_required
@rol_requerido(['medico'])  # o quien quieras permitir
def buscar_paciente(request):
    pacientes = []

    if request.method == 'POST':
        criterio = request.POST.get('dni')  # El input del formulario se llama 'dni'
        
        if criterio:
            # Busca por coincidencia exacta en DNI
            pacientes = Paciente.objects.filter(dni__icontains=criterio)

    return render(request, 'gestion/buscar_paciente.html', {'pacientes': pacientes})





@login_required
@rol_requerido(['medico'])
def lista_turnos(request):
    turnos = Turno.objects.all()
    return render(request, 'gestion/lista_turnos.html', {'turnos': turnos})


@login_required
@rol_requerido(['medico'])
def cargar_informe(request, paciente_id):
    paciente = get_object_or_404(Paciente, user_id=paciente_id)
    
    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.medico = request.user
            informe.paciente = paciente.user
            informe.save()
            return redirect('lista_turnos')
    else:
        form = InformeForm()

    return render(request, 'gestion/cargar_informe.html', {'form': form, 'paciente': paciente})


################

@login_required
@rol_requerido(['medico'])  # Solo los médicos pueden acceder
def historia_clinica(request, paciente_id):
    paciente = get_object_or_404(User, id=paciente_id)
    informes = Informe.objects.filter(paciente=paciente).order_by('-fecha')

    return render(request, 'gestion/historia_clinica.html', {
        'paciente': paciente,
        'informes': informes
    })


####################




@login_required
@rol_requerido(['medico'])
def panel_medico(request):
    turnos = Turno.objects.filter(medico=request.user)
    return render(request, 'gestion/panel_medico.html', {'turnos': turnos})


# --- PACIENTE ---
@login_required
@rol_requerido(['paciente'])
def ver_informe(request):
    informes = request.user.informes.all()
    return render(request, 'gestion/ver_informe.html', {'informes': informes})


@login_required
@rol_requerido(['paciente'])
def panel_paciente(request):
    informes = request.user.informes.all()
    return render(request, 'gestion/panel_paciente.html', {'informes': informes})


### ========== 4. OTROS ==========
@login_required
@rol_requerido(['medico', 'secretaria'])
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'gestion/lista_pacientes.html', {'pacientes': pacientes})


@login_required
def lista_usuarios(request):
    perfiles = Perfil.objects.all()
    return render(request, 'gestion/lista_usuarios.html', {'perfiles': perfiles})


def no_autorizado(request):
    return render(request, 'gestion/no_autorizado.html')
