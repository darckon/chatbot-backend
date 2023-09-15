# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos (requirements.txt) al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación (ajusta según tu aplicación)
EXPOSE 5000

# Define el comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "manage.py"]