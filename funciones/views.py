import urllib.parse
import google.generativeai as genai
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import funciones, Usuarios, MensajeChat, Tarea
from .serializer import funcionesSerializer, UsuariosSerializer, MensajeChatSerializer

class funcionesViewSet(viewsets.ModelViewSet):
    serializer_class = funcionesSerializer
    queryset = funciones.objects.all()

@api_view(['POST'])
def Login(request):
    password = request.data.get('password')
    username = request.data.get('username')
    user = get_object_or_404(Usuarios, username=username, password=password)
    if user:    
        return Response({
            'message': 'Login exitoso',
            'usuario_id': user.id 
        })        

@api_view(['POST'])
def Register(request):
    dato = UsuariosSerializer(data=request.data)
    if dato.is_valid():
        dato.save()
        return Response({'message': 'Usuario registrado exitosamente'})
    else:
        return Response(dato.errors, status=400)

@api_view(['GET'])
def obtener_historial(request, usuario_id):
    try:
        usuario = Usuarios.objects.get(id=usuario_id)
        mensajes = MensajeChat.objects.filter(usuario=usuario).order_by('fecha')
        serializer = MensajeChatSerializer(mensajes, many=True)
        return Response(serializer.data)
    except Usuarios.DoesNotExist:
        return Response([])

@api_view(['POST', 'GET'])
def manejar_tareas(request):
    # crear tarea
    if request.method == 'POST':
        usuario_id = request.data.get('usuario_id')
        titulo = request.data.get('titulo')
        fecha_limite = request.data.get('fecha_limite') 
        hora_limite = request.data.get('hora_limite') or None 

        usuario = get_object_or_404(Usuarios, id=usuario_id)
        
        nueva_tarea = Tarea.objects.create(
            usuario=usuario,
            titulo=titulo,
            fecha_limite=fecha_limite,
            hora_limite=hora_limite
        )

        return Response({"message": "Tarea agregada con éxito", "id": nueva_tarea.id})

    # tareas pendientes 
    elif request.method == 'GET':
        usuario_id = request.query_params.get('usuario_id')
        usuario = get_object_or_404(Usuarios, id=usuario_id)
        
        tareas_pendientes = Tarea.objects.filter(usuario=usuario, completada=False).order_by('fecha_limite')
        
        data = []
        for t in tareas_pendientes:
            data.append({
                "id": t.id,
                "titulo": t.titulo,
                "fecha": str(t.fecha_limite),
                "hora": str(t.hora_limite)[:5] if t.hora_limite else "" 
            })
        return Response(data)
    
@api_view(['PUT', 'DELETE'])
def detalle_tarea(request, tarea_id):
    # Buscamos la tarea por su ID único
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Eliminar tarea
    if request.method == 'DELETE':
        tarea.delete()
        return Response({"message": "Tarea eliminada con éxito"})

    # Modificar datos tarea
    elif request.method == 'PUT':
        tarea.titulo = request.data.get('titulo', tarea.titulo)
        tarea.fecha_limite = request.data.get('fecha_limite', tarea.fecha_limite)
        
        hora = request.data.get('hora_limite')
        tarea.hora_limite = hora if hora else None # Si viene vacío lo deja como None
        
        tarea.completada = request.data.get('completada', tarea.completada)
        tarea.save()
        
        return Response({"message": "Tarea actualizada con éxito"})

# PROCESAMIENTO DE CHAT Y GEMINI

genai.configure(api_key="INGRESA_TU_API_KEY_DE_GOOGLE_AQUI")  
modelo = genai.GenerativeModel('gemini-3.5-flash')

@api_view(['POST'])
def procesar_chat(request):
    mensaje = request.data.get('mensaje', '').lower()
    usuario_id = request.data.get('usuario_id') 

    # prueba de fallos
    try:
        usuario = Usuarios.objects.get(id=usuario_id)
    except Usuarios.DoesNotExist:
        usuario = Usuarios.objects.first()
        if not usuario:
            usuario = Usuarios.objects.create(username="admin_prueba", password="123", name="Admin")

    # Guardamos tu mensaje
    MensajeChat.objects.create(usuario=usuario, emisor="yo", texto=request.data.get('mensaje'))

    # musica
    palabras_musica = ["reproduce", "pon música", "escuchar", "abre"]
    if any(palabra in mensaje for palabra in palabras_musica):
        busqueda = mensaje
        palabras_a_limpiar = palabras_musica + ["en spotify", "spotify", "en youtube music", "youtube music", "youtube", "y"]
        for palabra in palabras_a_limpiar:
            busqueda = busqueda.replace(palabra, "").strip()
            
        query = urllib.parse.quote(busqueda)
        url_spotify = f"https://open.spotify.com/search/{query}"
        url_youtube = f"https://music.youtube.com/search?q={query}"

        if "spotify" in mensaje:
            respuesta = f"¡Enseguida! Buscando '{busqueda}' en Spotify..."
            MensajeChat.objects.create(usuario=usuario, emisor="tuke", texto=respuesta)
            return Response({"respuesta": respuesta, "accion": "abrir_musica", "plataforma": "spotify", "url_spotify": url_spotify})
            
        elif "youtube" in mensaje:
            respuesta = f"¡Enseguida! Buscando '{busqueda}' en YouTube Music..."
            MensajeChat.objects.create(usuario=usuario, emisor="tuke", texto=respuesta)
            return Response({"respuesta": respuesta, "accion": "abrir_musica", "plataforma": "youtube", "url_youtube": url_youtube})
            
        else:
            respuesta = f"Encontré '{busqueda}'. ¿Dónde prefieres escuchar esto?"
            MensajeChat.objects.create(usuario=usuario, emisor="tuke", texto=respuesta)
            return Response({"respuesta": respuesta, "accion": "abrir_musica", "plataforma": "opciones", "url_spotify": url_spotify, "url_youtube": url_youtube})

    # chat normal
    try:
        respuesta_ia = modelo.generate_content(mensaje)
        texto_tuke = respuesta_ia.text
        
        MensajeChat.objects.create(usuario=usuario, emisor="tuke", texto=texto_tuke)
        return Response({"respuesta": texto_tuke, "accion": "hablar"})
        
    except Exception as e:
        # Manejo de errores con estilo
        print(f"=============================================")
        print(f" TIPO DE ERROR: {type(e).__name__}")
        print(f" DETALLE DEL ERROR: {e}") 
        print(f"=============================================")
        
        error_msg = "Mmm, tuve un cruce de cables. ¿Me repites?"
        MensajeChat.objects.create(usuario=usuario, emisor="tuke", texto=error_msg)
        return Response({"respuesta": error_msg, "accion": "error"})