from django.db import models

class funciones(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
    
class Usuarios(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.username

# HISTORIAL DE CHAT
class MensajeChat(models.Model):
    # Enlazamos cada mensaje con un usuario específico de tu clase "Usuarios"
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="historial_chat")
    emisor = models.CharField(max_length=10) # Guardará "yo" o "tuke"
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True) # Guarda la fecha y hora automáticamente al crearse

    def __str__(self):
        return f"{self.usuario.username} - {self.emisor}: {self.texto[:20]}"

class Tarea(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="tareas")
    titulo = models.CharField(max_length=250)
    fecha_limite = models.DateField()
    hora_limite = models.TimeField(blank=True, null=True) # Puede ser opcional
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo} ({self.fecha_limite})"