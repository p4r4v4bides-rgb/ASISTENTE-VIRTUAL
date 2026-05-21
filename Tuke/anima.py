import sys
import random
import math 
import os
import webbrowser
import logging
import threading 
import subprocess
def ruta_recurso(ruta_relativa):
    try:
        # PyInstaller crea una carpeta temporal para los archivos empaquetados
        base_path = sys._MEIPASS
    except Exception:
        # Si no está empaquetado, usa la carpeta actual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, ruta_relativa)

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QPixmap, QTransform, QIcon, QAction
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject 
from flask import Flask, request
from flask_cors import CORS

# apagamos los logs de flask para no ensuciar la consola
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app_flask = Flask(__name__)
CORS(app_flask)

#  correr el servidor web
class ServidorWeb(QObject):
    senal_hablar = pyqtSignal(str)
    senal_mostrar = pyqtSignal()
    senal_ocultar = pyqtSignal()

    def iniciar(self):
        # daemon=True hace que el servidor se autodestruya al cerrar la app
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
            
        app_flask.run(port=5005, use_reloader=False)

#  La Burbuja de Texto 
class BurbujaTexto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.label = QLabel("", self)
        self.label.setStyleSheet("""
            background-color: white; 
            color: black; 
            border: 2px solid #333; 
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


# El animalito 
class animalitoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.burbuja = BurbujaTexto()
        self.frases = [
            "¡Hola! ¿Qué investigamos hoy?",
            "Recuerda tomar un poco de agua",
            "Tengo los ojos en tus tareas...",
            "Me pregunto de qué color me pondré hoy",
            "Sigue así, vas por buen camino",
            "Shhh... estoy concentrado",
            "«tchi-tchi-tchi», «que-que-que» o «ck-ck-ck»",
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
            "Más allá de no sé donde, tampoco se sabe cuándo, dicen que sale un espanto, que lo vieron no se sabe, ni dónde, ni cómo, ni cuandoni por qué andaba espantando",
            "Eres más fuerte de lo que piensas",
            "Los huesos de los tukekes, brillan en luz ultra violeta",
            "Quiero una double cheese & bacon",
            "To think about the girl you love and hold her tight, So happy together",
            "He-he"
            
        ]
        self.hablando = False 
        self.inicializarUI()
        self.configurar_bandeja()
        
        # INICIAR SERVER 
        self.servidor = ServidorWeb()
        self.servidor.senal_hablar.connect(self.decir_mensaje_custom)
        self.servidor.senal_mostrar.connect(self.aparecer_con_efecto)
        self.servidor.senal_ocultar.connect(self.secuencia_despedida)
        self.servidor.iniciar() # <--- Aquí usamos iniciar()

        # Ocultamos el "cuerpo"
        self.hide() # pa' forzar a que inicie oculto

        # Apagamos el "cerebro" para que el chistoso no hable antes de tiempo
        self.timer_animacion.stop() 
        self.timer_decision.stop()

    def aparecer_con_efecto(self):
        # Lo teletransportamos justo afuera de la pantalla por la izquierda
        self.pos_x = -200 
        self.pos_y = self.alto_pantalla // 2 # A la mitad de la altura de tu monitor
        self.move(int(self.pos_x), int(self.pos_y))
        
        self.show()
        
        # 2. Le ponemos velocidad máxima hacia la derecha
        self.vel_x = 30 
        self.vel_y = 0
        self.timer_animacion.setInterval(40) # Patitas a toda velocidad
        self.timer_animacion.start()
        self.timer_decision.start(2000)
        self.actualizar_mirada() # Lo obligamos a mirar a la derecha
        
        # 3. Le damos 1 segundo para que entre a la pantalla, se frene y salude
        QTimer.singleShot(1000, self.saludar_llegada)

    def saludar_llegada(self):
        # La función decir_mensaje_custom ya se encarga de frenarlo automáticamente
        self.decir_mensaje_custom("¡Zzz... Ah! ¡Hola! Ya estoy aquí.")

    def decir_mensaje_custom(self, texto):
        self.hablando = True
        self.vel_x = 0
        self.vel_y = 0
        self.timer_decision.stop() 
        self.timer_animacion.setInterval(250) 
        self.burbuja.mostrar_mensaje(texto, self.pos_x, self.pos_y, self.width(), self.height())
        tiempo_lectura = max(3500, len(texto) * 100) # Calcula el tiempo según lo largo del texto
        self.timer_habla.start(int(tiempo_lectura))

    # provisional por si queremos q haga algo en ese click derechoo
    def secuencia_despedida(self):
        # detenemos al tuke para que hable
        self.hablando = True
        self.vel_x = 0
        self.vel_y = 0
        self.timer_decision.stop() 
        
        # mostramos el mensaje
        mensaje = "¡Me voy a descansar! Adiós."
        self.burbuja.mostrar_mensaje(mensaje, self.pos_x, self.pos_y, self.width(), self.height())
        
        # programamos el apagado para dentro de 3 segundos
        QTimer.singleShot(2500, self.apagar_tukeke)

    def apagar_tukeke(self): #apagar anima
        # Apaga todo sin cerrar el programa por completo
        self.hide() 
        self.burbuja.hide() 
        self.hablando = False
        self.timer_animacion.stop() 
        self.timer_decision.stop()
    #imagenes del bichin
    def inicializarUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label = QLabel(self)
        
        # posicion del animalito 
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ordenamos los frames para crear un ciclo fluido de caminata
        ruta_base = os.path.dirname(os.path.abspath(__file__))

        nombres_archivos = [
        os.path.join(ruta_base, "imagen", "paso_adelante.png"),
        os.path.join(ruta_base, "imagen", "paso_quieto.png"),
        os.path.join(ruta_base, "imagen", "paso_atras.png"),
        os.path.join(ruta_base, "imagen", "paso_quieto.png")
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
        # crear el ícono de la bandeja
        self.tray_icon = QSystemTrayIcon(self)
        
        # Le asignamos tu archivo icono.ico usando nuestra brújula
        ruta_icono = ruta_recurso("icono.ico") # <--- USAMOS LA FUNCIÓN NUEVA
        self.tray_icon.setIcon(QIcon(ruta_icono))

        # Crear el menú de opciones (el que sale con clic derecho)
        tray_menu = QMenu()

        # Opción para Despertarlo
        accion_despertar = tray_menu.addAction("Despertar Tukeke")
        accion_despertar.triggered.connect(self.aparecer_con_efecto)

        # Opción para Dormirlo
        accion_dormir = tray_menu.addAction("Dormir Tukeke")
        accion_dormir.triggered.connect(self.secuencia_despedida)

        # Un separador visual (una rayita)
        tray_menu.addSeparator()

        # Opción para Salir (cierra el programa definitivamente)
        accion_salir = tray_menu.addAction("Cerrar por completo")
        accion_salir.triggered.connect(QApplication.quit)

        # Asignar el menú al ícono y mostrarlo en la barra de tareas
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
        self.timer_habla.start(3500) 

    def terminar_hablar(self):
        self.burbuja.hide() 
        self.hablando = False
        self.timer_decision.start(1000) 
        self.cambiar_direccion() 

    # Busqueda del tamaño maximo para evitar cortes 
    def actualizar_mirada(self):
        if self.vel_x == 0 and self.vel_y == 0:
            return

        angulo = math.degrees(math.atan2(self.vel_y, self.vel_x))

        self.sprites_actuales = []
        max_ancho = 0
        max_alto = 0

        # Rotamos las imágenes
        for pixmap_base in self.frames_base:
            transform = QTransform()
            if self.vel_x < 0:
                transform.scale(1, -1) # Evita que quede patas arriba

            transform.rotate(angulo)
            pixmap_rotado = pixmap_base.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            
            if pixmap_rotado.width() > max_ancho: max_ancho = pixmap_rotado.width()
            if pixmap_rotado.height() > max_alto: max_alto = pixmap_rotado.height()
            
            self.sprites_actuales.append(pixmap_rotado)

        # guardamos el centro exacto donde está parado el animalito ahora
        centro_x = self.pos_x + (self.width() / 2)
        centro_y = self.pos_y + (self.height() / 2)

        # aplicamos los nuevos tamaños de la caja rotada
        self.resize(max_ancho, max_alto)
        self.label.resize(max_ancho, max_alto)
        
        # recalculamos la esquina (pos_x, pos_y) empujandola hacia atrás
        # para que el centro siga siendo exactamente el mismo
        self.pos_x = centro_x - (max_ancho / 2)
        self.pos_y = centro_y - (max_alto / 2)
        
        # movemos la ventana fisicamente para compensar el crecimiento
        self.move(int(self.pos_x), int(self.pos_y))

        # asignamos la imagen correcta
        self.label.setPixmap(self.sprites_actuales[self.frame_actual])
        
        # que salga de One el animalito
        self.label.repaint()
        QApplication.processEvents()

    def actualizar_frame(self):
        
        # Si se está moviendo o hablando, hace el ciclo normal de animación
        if self.vel_x != 0 or self.vel_y != 0 or self.hablando:
            self.frame_actual += 1
            if self.frame_actual >= len(self.sprites_actuales):
                self.frame_actual = 0
            self.label.setPixmap(self.sprites_actuales[self.frame_actual])
        else:
            # Si está completamente quieto, forzamos el frame "paso_quieto"
            self.frame_actual = 1
            self.label.setPixmap(self.sprites_actuales[self.frame_actual])

        # aplicamos el movimiento
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        # teletransporte 
        margen = 20 # Le damos un margen para que cruce la pantalla por completo
        
        # Si sale por la DERECHA -> Aparece en la IZQUIERDA
        if self.pos_x > self.ancho_pantalla + margen: 
            self.pos_x = -(self.width() / 2) # Asoma la mitad del cuerpo
            if self.vel_x <= 0: 
                self.vel_x = random.choice([2, 3]) # lo obligamos a entrar
            
        # Si sale por la IZQUIERDA -> Aparece en la DERECHA
        elif self.pos_x < -self.width() - margen: 
            self.pos_x = self.ancho_pantalla - (self.width() / 2)
            if self.vel_x >= 0: 
                self.vel_x = random.choice([-2, -3]) # lo obligamos a entrar

        # Si sale por ABAJO -> Aparece ARRIBA
        if self.pos_y > self.alto_pantalla + margen: 
            self.pos_y = -(self.height() / 2)
            if self.vel_y <= 0: 
                self.vel_y = random.choice([2, 3])
            
        # Si sale por ARRIBA -> Aparece ABAJO
        elif self.pos_y < -self.height() - margen: 
            self.pos_y = self.alto_pantalla - (self.height() / 2)
            if self.vel_y >= 0: 
                self.vel_y = random.choice([-2, -3])

        # Mover la ventana a la nueva posición recalculada
        self.move(int(self.pos_x), int(self.pos_y))
    # susto del click 
    def mousePressEvent(self, event):
        # Clic derecho lo manda a dormir
        if event.button() == Qt.MouseButton.RightButton:
            self.apagar_tukeke()
                
        # clic en la rueda del ratón lo cierra por completo
        elif event.button() == Qt.MouseButton.MiddleButton:
            QApplication.quit() # Mata el programa
            
        # Clic izquierdo lo asusta
        elif event.button() == Qt.MouseButton.LeftButton:
            
            # si estaba hablando, se calla del susto
            if self.hablando:
                self.burbuja.hide()
                self.hablando = False

            # forzamos el MODO SPRINT (Huida)
            opciones_rapidas = [-25, -20, 20, 25] # Aún más rápido por el susto
            self.vel_x = random.choice(opciones_rapidas)
            self.vel_y = random.choice([-20, -15, 15, 20]) 
            
            # aceleramos sus patitas
            self.timer_animacion.setInterval(40) 
            
            # reiniciamos su cerebro para que corra por 800ms y luego se calme
            self.timer_decision.start(800) 
            
            # forzamos la rotación inmediata para que no haga Moonwalk
            self.actualizar_mirada()

# Variables globales para guardar los procesos y poder cerrarlos después
proceso_django = None
proceso_frontend = None

def limpiar_procesos():
    # Usamos taskkill con /T (Tree/Árbol) para aniquilar toda la cadena de sub-procesos en Windows
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) 
    
    # AUTOMATIZACIÓN DE SERVIDORES 
    # Truco para que el .exe sepa dónde está parado:
    if getattr(sys, 'frozen', False):
        # Si el programa está empaquetado como .exe, busca la ruta del .exe
        ruta_tuke = os.path.dirname(sys.executable)
    else:
        # Si lo corres normal desde el editor, busca la ruta del .py
        ruta_tuke = os.path.dirname(os.path.abspath(__file__))
        
    ruta_raiz = os.path.abspath(os.path.join(ruta_tuke, "..")) # Sube a ASISTENTE-VIRTUAL
    ruta_frontend = os.path.join(ruta_raiz, "Frontend")
    
    # ejecutar Base de Datos (Django)
    ruta_python_venv = os.path.join(ruta_raiz, "venv", "Scripts", "python.exe")
    ruta_manage = os.path.join(ruta_raiz, "manage.py")
    
    if os.path.exists(ruta_python_venv) and os.path.exists(ruta_manage):
        # Enciende Django silenciosamente en segundo plano
        proceso_django = subprocess.Popen([ruta_python_venv, ruta_manage, "runserver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    # ejecutar Frontend (Vite)
    if os.path.exists(ruta_frontend):
        # Enciende Node/Vite simulando la terminal dentro de la carpeta Frontend
        proceso_frontend = subprocess.Popen("npm run dev", cwd=ruta_frontend, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    # conectamos la limpieza para que no queden procesos fantasma al salir
    app.aboutToQuit.connect(limpiar_procesos)

    ventana = animalitoApp()
    
    # Le damos 2 segundos a los servidores para que arranquen bien antes de abrir el navegador
    QTimer.singleShot(2000, lambda: webbrowser.open("http://localhost:5173"))
    
    sys.exit(app.exec())