FROM python:latest

# Copiar las librerias a usar al contenedor
ADD requirements.txt requirements.txt
# Instalar
RUN pip install -r requirements.txt

####################################
# Copiar ficheros (para Kubernetes)
# COPY ./src /root/app
####################################


# Inicio
CMD ["python", "-u", "app.py"]