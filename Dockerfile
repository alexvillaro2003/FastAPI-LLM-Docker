# Imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt a la imagen
COPY requirements.txt /app/

# Instalar las dependencias necesarias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos de la aplicación al contenedor
COPY . /app/

# Exponer el puerto en el que FastAPI estará escuchando (por defecto 8000)
EXPOSE 8000

# Comando para ejecutar el servidor FastAPI utilizando Uvicorn
CMD ["uvicorn", "api_model:app", "--host", "0.0.0.0", "--port", "8000"]
