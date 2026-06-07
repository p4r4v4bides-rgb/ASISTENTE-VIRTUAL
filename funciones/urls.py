from django.urls import path, include
from rest_framework import routers
from funciones import views

router = routers.DefaultRouter()
router.register(r'funciones', views.funcionesViewSet,'funciones')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("login/", views.Login),
    path("register/", views.Register),
    path('api/chat/', views.procesar_chat, name='procesar_chat'),
    path('api/historial/<int:usuario_id>/', views.obtener_historial, name='obtener_historial'),
    path('api/tareas/', views.manejar_tareas, name='manejar_tareas'),
]

