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
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.username
