import sys
import random
import math 
import os
import logging
import threading 
import subprocess

def ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, ruta_relativa).replace("\\", "/")

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QPixmap, QTransform, QIcon, QAction
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QUrl 
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput 
from flask import Flask, request
from flask_cors import CORS

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app_flask = Flask(__name__)
CORS(app_flask)

class ServidorWeb(QObject):
    senal_hablar = pyqtSignal(str)
    senal_mostrar = pyqtSignal()
    senal_ocultar = pyqtSignal()

    def iniciar(self):
        hilo = threading.Thread(target=self.correr_flask, daemon=True)
        hilo.start()

    def correr_flask(self):
        @app_flask.route('/despertar', methods=['POST'])
        def despertar():
            self.senal_mostrar.emit()
            return {"status": "ok"}
        @app_flask.route('/dormir', methods=['POST'])
        def dormir():
            self.senal_ocultar.emit()
            return {"status": "ok"}

        @app_flask.route('/hablar', methods=['POST'])
        def hablar():
            datos = request.json
            mensaje = datos.get('mensaje', '¡Hola!')
            self.senal_hablar.emit(mensaje)
            return {"status": "ok"}
            
        try:
            app_flask.run(port=5005, use_reloader=False)
        except Exception:
            pass 

class BurbujaTexto(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.SubWindow | 
            Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.label = QLabel("", self)
        self.label.setStyleSheet("""
            background-color: white; 
            color: black; 
            border: 2px solid #333333; 
            border-radius: 10px; 
            padding: 8px; 
            font-weight: bold; 
            font-family: Arial;
        """)
        self.label.setWordWrap(True)

    def mostrar_mensaje(self, texto, chami_x, chami_y, chami_ancho, chami_alto):
        self.label.setText(texto)
        self.label.adjustSize()
        self.resize(self.label.width(), self.label.height())
        
        pantalla = QApplication.primaryScreen().geometry()
        ancho_monitor = pantalla.width()
        
        pos_x = int((chami_x + (chami_ancho / 2)) - (self.width() / 2))
        pos_y = chami_y - self.height() - 10 

        if pos_x + self.width() > ancho_monitor: pos_x = ancho_monitor - self.width() - 10
        if pos_x < 0: pos_x = 10
        if pos_y < 0: pos_y = chami_y + chami_alto + 10

        self.move(int(pos_x), int(pos_y))
        self.show()

class animalitoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.burbuja = BurbujaTexto()
        self.frases = [
            "«tchi-tchi-tchi», «que-que-que» o «ck-ck-ck»",
            "¡Hola! ¿Qué investigamos hoy?",
            "Recuerda tomar un poco de agua",
            "Tengo los ojos en tus tareas...",
            "Me pregunto de qué color me pondré hoy",
            "Sigue así, vas por buen camino",
            "Shhh... estoy concentrado",
            "E=mc², pero yo soy más de E=tuKe²",
            "Animo, animo, animo, animo, a-animo, a-animo, animo, animo, a-animo, a-animo, animo...",
            "En ocaciones, checa mi mookwalk",
            "Programadores flojos, aun no me dan mi propia serie de Netflix",
            "Chambea jala, siga estudiando, no te me rajes, que el tuke te acompaña",
            "Gu-yi-bi-fan, siga chambeando",
            "Antes iba a ser un camaleon, pero esos son feos, mejor un tukeke",
            "Guyana nos pertenece",
            "Para cuando me daran una mejorita",
            "Denme un Ds",
            "¿Sabías que el tuke es el animalito más rápido del mundo? Bueno, al menos en esta pantalla",
            "No me clickees, soy tímido",
            "Las campanas de la iglesia estan sonando, anunciando que el tuke esta llegando",
            "Pongan musica",
            "Bendita la luz, bendita la luz de tu mirada",
            "Oppa gangnam style",
            "Por que té de-moras",
            "凡是讀到這段話的人都是同性戀。",
            "La disciplina es el puente entre tus metas y tus logros. ¡Sigue así!",
            "Si fuera fácil, cualquiera lo haría. Estás demostrando de qué estás hecho",
            "Confía en ti y en las horas que le has dedicado. ¡Tú puedes con esto!",
            "Un examen no define quién eres, pero tu dedicación de estos días me dice que vas a salir genial",
            "Los retos más grandes preparan a las personas comunes para destinos extraordinarios",
            "Cada hora de estudio de hoy es una puerta que se abrirá mañana",
            "No se trata de ser el mejor de todos, se trata de ser mejor de lo que eras ayer",
            "Little patience, yeah, yeah",
            "Oye, abre tus ojos, mira hacia arriba, disfruta las cosas buenas que tiene la vida",
            "Creo en mí, en lo que puedo hacer, no hay nada que me dé más fuerza",
            "Los mejores mundiales, con las mejores canciones de mundiales, 2010, 2014, el resto meh",
            "Más allá de no sé donde, tampoco se sabe cuándo, dicen que sale un espanto, que lo vieron no se sabe, ni dónde, ni cómo, ni cuando, ni por qué andaba espantando",
            "Eres más fuerte de lo que piensas",
            "Los huesos de los tukekes, brillan en luz ultra violeta",
            "Quiero una double cheese & bacon",
            "To think about the girl you love and hold her tight, So happy together",
            "He-he"
            
        ]
        self.hablando = False 

        self.reproductor = QMediaPlayer()
        self.salida_audio = QAudioOutput()
        self.reproductor.setAudioOutput(self.salida_audio)
        self.salida_audio.setVolume(1.0) # Volumen al 100%

        self.inicializarUI()
        self.configurar_bandeja()
        
        self.servidor = ServidorWeb()
        self.servidor.senal_hablar.connect(self.decir_mensaje_custom)
        self.servidor.senal_mostrar.connect(self.aparecer_con_efecto)
        self.servidor.senal_ocultar.connect(self.secuencia_despedida)
        self.servidor.iniciar() 

        self.hide() 

        self.timer_animacion.stop() 
        self.timer_decision.stop()

    def aparecer_con_efecto(self):
        self.pos_x = -200 
        self.pos_y = self.alto_pantalla // 2 
        self.move(int(self.pos_x), int(self.pos_y))
        
        self.show()
        
        self.vel_x = 30 
        self.vel_y = 0
        self.timer_animacion.setInterval(40)
        self.timer_animacion.start()
        self.timer_decision.start(2000)
        self.actualizar_mirada() 
        
        QTimer.singleShot(1000, self.saludar_llegada)

    def saludar_llegada(self):
        self.decir_mensaje_custom("¡Zzz... Ah! ¡Hola! Ya estoy aquí.")
    
    def verificar_sonido(self, texto):
        texto_min = texto.lower()
        # Si encuentra alguna de las onomatopeyas en el texto, reproduce el audio
        if "tchi-tchi-tchi" in texto_min or "que-que-que" in texto_min or "ck-ck-ck" in texto_min:
            # Asegúrate de que el archivo 'onomatopeya.m4a' esté en la misma carpeta que tu script
            ruta_audio = ruta_recurso("extras/onomatopeya.m4a") 
            self.reproductor.setSource(QUrl.fileURLWithPath(ruta_audio))
            self.reproductor.play()

    def decir_mensaje_custom(self, texto):
        self.hablando = True
        self.vel_x = 0
        self.vel_y = 0
        self.timer_decision.stop() 
        self.timer_animacion.setInterval(250) 
        self.burbuja.mostrar_mensaje(texto, self.pos_x, self.pos_y, self.width(), self.height())
        tiempo_lectura = max(3500, len(texto) * 100)
        self.timer_habla.start(int(tiempo_lectura))

    def secuencia_despedida(self):
        self.hablando = True
        self.vel_x = 0
        self.vel_y = 0
        self.timer_decision.stop() 
        self.timer_habla.stop()
        
        mensaje = "¡Me voy a descansar! Adiós."
        self.burbuja.mostrar_mensaje(mensaje, self.pos_x, self.pos_y, self.width(), self.height())
        
        QTimer.singleShot(2500, self.apagar_tukeke)

    def apagar_tukeke(self): 
        self.hide() 
        self.burbuja.hide() 
        self.hablando = False
        self.timer_animacion.stop() 
        self.timer_decision.stop()
        self.timer_habla.stop()
        
    def inicializarUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.SubWindow | 
            Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        nombres_archivos = [
        ruta_recurso("extras/paso_adelante.png"),
        ruta_recurso("extras/paso_quieto.png"),
        ruta_recurso("extras/paso_atras.png"),
        ruta_recurso("extras/paso_quieto.png")
        ]
        
        self.frames_base = [] 
        
        for nombre in nombres_archivos:
            pixmap = QPixmap(nombre).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.frames_base.append(pixmap)
    
        self.sprites_actuales = self.frames_base.copy()
        self.frame_actual = 0 
        
        self.label.setPixmap(self.sprites_actuales[self.frame_actual])
        
        self.resize(150, 150)
        self.label.resize(150, 150)

        pantalla = QApplication.primaryScreen().geometry()
        self.ancho_pantalla = pantalla.width()
        self.alto_pantalla = pantalla.height()

        self.pos_x = 0
        self.pos_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.move(self.pos_x, self.pos_y)

        self.timer_animacion = QTimer(self)
        self.timer_animacion.timeout.connect(self.actualizar_frame) 
        self.timer_animacion.start(150)

        self.timer_decision = QTimer(self)
        self.timer_decision.timeout.connect(self.cambiar_direccion)
        self.timer_decision.start(2000)

        self.timer_habla = QTimer(self)
        self.timer_habla.setSingleShot(True) 
        self.timer_habla.timeout.connect(self.terminar_hablar)

    def configurar_bandeja(self):
        self.tray_icon = QSystemTrayIcon(self)
        ruta_icono = ruta_recurso("extras/icono.ico") 
        self.tray_icon.setIcon(QIcon(ruta_icono))

        tray_menu = QMenu()

        accion_despertar = tray_menu.addAction("Despertar Tukeke")
        accion_despertar.triggered.connect(self.aparecer_con_efecto)

        accion_dormir = tray_menu.addAction("Dormir Tukeke")
        accion_dormir.triggered.connect(self.secuencia_despedida)

        tray_menu.addSeparator()

        accion_salir = tray_menu.addAction("Cerrar por completo")
        accion_salir.triggered.connect(QApplication.quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def cambiar_direccion(self):
        if self.hablando: return

        puede_hablar = (
            self.pos_x > 0 and 
            self.pos_x < (self.ancho_pantalla - 150) and 
            self.pos_y > 100 and 
            self.pos_y < (self.alto_pantalla - 150)
        )

        probabilidad = random.random()

        if probabilidad < 0.15 and puede_hablar:
            self.iniciar_habla()
        elif probabilidad < 0.70: 
            opciones_lentas = [-3, -2, -1, 0, 0, 1, 2, 3] 
            self.vel_x = random.choice(opciones_lentas)
            self.vel_y = random.choice(opciones_lentas)
            self.timer_animacion.setInterval(150) 
            self.timer_decision.setInterval(random.randint(3000, 6000)) 
        else:
            opciones_rapidas = [-20, -15, 15, 20]
            self.vel_x = random.choice(opciones_rapidas)
            self.vel_y = random.choice([-20, -15, 15, 20]) 
            self.timer_animacion.setInterval(40) 
            self.timer_decision.setInterval(800) 

        self.actualizar_mirada()

    def iniciar_habla(self):
        self.hablando = True
        self.vel_x = 0
        self.vel_y = 0
        self.timer_decision.stop() 
        self.timer_animacion.setInterval(250) 
        frase_elegida = random.choice(self.frases)
        self.burbuja.mostrar_mensaje(frase_elegida, self.pos_x, self.pos_y, self.width(), self.height())
        tiempo_lectura = max(4500, len(frase_elegida) * 100) 
        self.timer_habla.start(int(tiempo_lectura))

    def terminar_hablar(self):
        self.burbuja.hide() 
        self.hablando = False
        self.timer_decision.start(1000) 
        self.cambiar_direccion() 

    def actualizar_mirada(self):
        if self.vel_x == 0 and self.vel_y == 0:
            return

        angulo = math.degrees(math.atan2(self.vel_y, self.vel_x))

        self.sprites_actuales = []
        max_ancho = 0
        max_alto = 0

        for pixmap_base in self.frames_base:
            transform = QTransform()
            if self.vel_x < 0:
                transform.scale(1, -1) 

            transform.rotate(angulo)
            pixmap_rotado = pixmap_base.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            
            if pixmap_rotado.width() > max_ancho: max_ancho = pixmap_rotado.width()
            if pixmap_rotado.height() > max_alto: max_alto = pixmap_rotado.height()
            
            self.sprites_actuales.append(pixmap_rotado)

        centro_x = self.pos_x + (self.width() / 2)
        centro_y = self.pos_y + (self.height() / 2)

        self.resize(max_ancho, max_alto)
        self.label.resize(max_ancho, max_alto)
        
        self.pos_x = centro_x - (max_ancho / 2)
        self.pos_y = centro_y - (max_alto / 2)
        
        self.move(int(self.pos_x), int(self.pos_y))

        self.label.setPixmap(self.sprites_actuales[self.frame_actual])

    def actualizar_frame(self):
        if self.vel_x != 0 or self.vel_y != 0 or self.hablando:
            self.frame_actual += 1
            if self.frame_actual >= len(self.sprites_actuales):
                self.frame_actual = 0
        else:
            self.frame_actual = 1
            
        self.label.setPixmap(self.sprites_actuales[self.frame_actual])

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        margen = 20 
        
        if self.pos_x > self.ancho_pantalla + margen: 
            self.pos_x = -(self.width() / 2) 
            if self.vel_x <= 0: 
                self.vel_x = random.choice([2, 3]) 
            
        elif self.pos_x < -self.width() - margen: 
            self.pos_x = self.ancho_pantalla - (self.width() / 2)
            if self.vel_x >= 0: 
                self.vel_x = random.choice([-2, -3]) 

        if self.pos_y > self.alto_pantalla + margen: 
            self.pos_y = -(self.height() / 2)
            if self.vel_y <= 0: 
                self.vel_y = random.choice([2, 3])
            
        elif self.pos_y < -self.height() - margen: 
            self.pos_y = self.alto_pantalla - (self.height() / 2)
            if self.vel_y >= 0: 
                self.vel_y = random.choice([-2, -3])

        self.move(int(self.pos_x), int(self.pos_y))
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.apagar_tukeke()
                
        elif event.button() == Qt.MouseButton.MiddleButton:
            QApplication.quit() 
            
        elif event.button() == Qt.MouseButton.LeftButton:
            
            if self.hablando:
                self.burbuja.hide()
                self.hablando = False

            opciones_rapidas = [-25, -20, 20, 25] 
            self.vel_x = random.choice(opciones_rapidas)
            self.vel_y = random.choice([-20, -15, 15, 20]) 
            
            self.timer_animacion.setInterval(40) 
            self.timer_decision.start(800) 
            self.actualizar_mirada()

proceso_django = None
proceso_frontend = None

def limpiar_procesos():
    if proceso_django:
        try:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(proceso_django.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
            
    if proceso_frontend:
        try:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(proceso_frontend.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
def iniciar_habla(self):
        self.hablando = True
        self.vel_x = 0
        self.vel_y = 0
        self.timer_decision.stop() 
        self.timer_animacion.setInterval(250) 
        
        frase_elegida = random.choice(self.frases)
        
        self.verificar_sonido(frase_elegida) # <-- AÑADIMOS EL DETECTOR AQUÍ
        
        self.burbuja.mostrar_mensaje(frase_elegida, self.pos_x, self.pos_y, self.width(), self.height())
        tiempo_lectura = max(4500, len(frase_elegida) * 100) 
        self.timer_habla.start(int(tiempo_lectura))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) 
    
    if getattr(sys, 'frozen', False):
        ruta_tuke = os.path.dirname(sys.executable)
    else:
        ruta_tuke = os.path.dirname(os.path.abspath(__file__))
        
    ruta_raiz = os.path.abspath(os.path.join(ruta_tuke, ".."))
    ruta_frontend = os.path.join(ruta_raiz, "Frontend")
    
    ruta_python_venv = os.path.join(ruta_raiz, "venv", "Scripts", "python.exe")
    ruta_manage = os.path.join(ruta_raiz, "manage.py")
    
    CREATE_NO_WINDOW = 0x08000000 
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    BANDERAS = CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
    
    if os.path.exists(ruta_python_venv) and os.path.exists(ruta_manage):
        proceso_django = subprocess.Popen([ruta_python_venv, ruta_manage, "runserver"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=BANDERAS)
        
    if os.path.exists(ruta_frontend):
        proceso_frontend = subprocess.Popen("npm run dev", cwd=ruta_frontend, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=BANDERAS)
        
    app.aboutToQuit.connect(limpiar_procesos)

    ventana = animalitoApp()
    
    QTimer.singleShot(2000, lambda: os.startfile("http://localhost:5173"))
    
    sys.exit(app.exec())