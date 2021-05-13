FROM python:latest

# Instalar dependencias
ADD requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

#######################################
# Copiar ficheros (para Kubernetes)
# COPY ./src /root/app-web
#######################################

# Inicio
ENV FLASK_APP=app.py
CMD ["python", "-u", "app.py"]