from rest_framework import serializers
from .models import funciones,Usuarios

class funcionesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = funciones
        fields = '__all__'
        
        #fields = ['id', 'titulo', 'descripcion', 'done']

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'