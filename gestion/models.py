from django.db import models
from django.contrib.auth.models import User




class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"



class Turno(models.Model):
    ESTUDIOS = [
        ('resonancia', 'Resonancia'),
        ('tomografia', 'Tomografía'),
        ('ecografia', 'Ecografía'),
    ]
                                                                                                    #ForeignKey: vincula un turno con un paciente.
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos_paciente')    #on_delete=models.CASCADE: si se elimina un paciente, también se eliminan sus turnos
    medico = models.ForeignKey(User, related_name='turnos_medico', on_delete=models.CASCADE)
    estudio = models.CharField(max_length=20, choices=ESTUDIOS)                                       #choices: limita los estudios a un listado de opciones  
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.paciente} - {self.estudio} el {self.fecha} a las {self.hora}"




class Perfil(models.Model):
    ROLES = [
        ('secretaria', 'Secretaria'),
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - ({self.rol})"
    
  
    

  
class Informe(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='informes')
    medico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='informes_medico')
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Informe de {self.paciente.username} - {self.fecha}"
    
