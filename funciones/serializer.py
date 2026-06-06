from rest_framework import serializers
from .models import funciones,Usuarios, MensajeChat

class funcionesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = funciones
        fields = '__all__'
        
        #fields = ['id', 'titulo', 'descripcion', 'done']

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

class MensajeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = ['emisor', 'texto', 'fecha']