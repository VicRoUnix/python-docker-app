#Imagen de python quqe usaremos para el proyecto
FROM python:3.11-slim

# Directorio en el que trabajara la aplicacion en el contenedor 
WORKDIR /app

# Copiamos los requisitos 
COPY requirements.txt .

# Instalamos los requisitos
RUN pip install -r requirements.txt

# Copiamos los demas archivos para crear la imagen\
COPY . .

# Exponemos el puerto donde correra la aplicacion
EXPOSE 5000

# Ejecutamos la aplicacion app.py
CMD ["python", "app.py"]
