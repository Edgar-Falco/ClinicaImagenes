#Hacemos los formulario de turnos
from django import forms                    
from .models import Paciente, Turno, Perfil, Informe
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm




class PacienteForm(forms.ModelForm):    #forms.ModelForm es una forma rápida de generar formularios basados en tus modelos
    class Meta:
        model = Paciente                #model = Paciente o Turno: le decimos a Django qué modelo representa ese formulario.
        fields = '__all__'              #fields = '__all__': le pedimos que incluya todos los campos del modelo en el formulario.


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'


#Crear formulario de loggin
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=Perfil.ROLES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        


class RegistroForm(UserCreationForm):
    dni = forms.CharField(max_length=15, required=True)
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]





class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
        }