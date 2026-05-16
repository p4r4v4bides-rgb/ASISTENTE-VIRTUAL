from django.shortcuts import render
from rest_framework import viewsets
from .serializer import funcionesSerializer
from .models import funciones,Usuarios
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializer import UsuariosSerializer

# Create your views here.
class funcionesViewSet(viewsets.ModelViewSet):
    serializer_class = funcionesSerializer
    queryset = funciones.objects.all()

@api_view(['POST'])
def Login(request):
    password=request.data['password']
    username=request.data['username']
    user=get_object_or_404(Usuarios,username=username,password=password)
    if user:    
        return Response({'message':'Login exitoso'})        


@api_view(['POST'])
def Register(request):
    dato=UsuariosSerializer(data=request.data)
    if dato.is_valid():
        dato.save()
        return Response({'message':'Usuario registrado exitosamente'})
    else:
        return Response(dato.errors, status=400)
    

