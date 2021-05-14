# Imagen de Unix/Python de tamaño reducido
FROM python:3.9.5-slim-buster

# Copiar las librerias a usar al contenedor
ADD requirements.txt requirements.txt

# Adaptar componentes de Unix para la imagen slim
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip3 install --upgrade pip

# Instalar dependencias
RUN pip install -r requirements.txt

####################################
# Copiar ficheros (para Kubernetes)
# COPY ./src /root/app
####################################


# Inicio
CMD ["python", "-u", "app.py"]