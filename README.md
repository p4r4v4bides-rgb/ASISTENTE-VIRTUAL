🦎🦎🦎 Cómo encender a Tuke por primera vez (Leer antes de ejecutar)🦎🦎🦎

mi gente peru, cuando descarguen o clonen el proyecto de GitHub, el programa no va a funcionar de una vez si solo le dan doble clic al .exe. Esto pasa porque GitHub ignora y no descarga las carpetas pesadas (node_modules del frontend ni venv del backend).

Paso 1: Frontend
Para instalar los modulos del frond

cd Frontend

npm install

Paso 2: Backend
En esa misma terminal (asegúrense de haber vuelto a la carpeta ASISTENTE-VIRTUAL), vamos a crear el entorno virtual de Python y a descargar las librerías

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

Paso 3:

python manage.py migrate

python manage.py createsuperuser

