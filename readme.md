# ¿Qué es esto?
Este repositorio contiene un ejemplo de arquitectura de microservicios creado con Docker.

El proyecto consta de 3 microservicios editables: (1) un proceso en background que añade números a una base de datos, (2) una web que muestra el número de registros que tiene la DB y (3) una DB persistente.

Gráfico con la arquitectura planteada:
![Arquitectura](/_architecture/architecture.png)

## Lanzar proyecto con Docker (docker-compose)
La arquitectura planteada se ha definido con **Docker Composer**.

1. **Lanzamiento (con build)**. Ejecución de Docker con Build completo (evitando cache)
`docker-compose up --force-recreate`

2. **Lanzamiento (basico)**. Una vez construidas las imagenes, se puede usar `up` directamente para lanzar las instancias. Su ejecución muestra el *output* en terminal de la consola.
`docker-compose up`

3. **Lanzamiento (silent)**. La opción `d` lanza las instancias y desconecta de la terminal. Es decir, la ejecución no muestra *output* en la consola.
`docker-compose up -d`

## Combinación con Kubernetes
Para desplegar este proyecto **Docker con Kubernetes**, seguir estos pasos:

1. Habilitar *Kubernetes* en *Docker Desktop*. Seguir la [documentación de Docker](https://docs.docker.com/desktop/kubernetes/#enable-kubernetes).

2. Adaptar los *Dockerfile*, de los microservicios creados, para generar imagenes aptas para Kubernetes de forma más sencilla. Recurrir a los ficheros `app/Dockerfile` y `app-web/Dockerfile`. **Descomentar** las líneas marcadas.

3. **Reconstruir** las imágenes de los microservicios: `docker-compose build --force-rm`.

4. Generar un fichero *docker-compose* con las variables de entorno traducidas. Ejecutar: `docker-compose config > docker-compose-resolved.yaml`.

5. **Modificar y adaptar** el fichero *docker-compose* resuelto, para adaptar al programa de traducción a Kubernetes y, ya de paso, para borrar lo que no funcionará en Kubernetes.

Acciones:
  - Cambiar el valor de la etiqueta `version` a `3.7`. *¿Por qué?* La version `3.8` de *docker-compose* no está disponible *todavía* en kompose.
  - Borrar las referencias a `depends-on`. *¿Por qué?* No están admitidas en kubernetes.

6. Crear una carpeta dedicada para los ficheros traducidos. Por ejemplo `config_for_kubernetes/`.

7. Traducir el fichero `docker-compose-resolved.yml` a los ficheros de *deploy*, *service* y *persistance* requeridos por Kubernetes.
  - La traducción se hace con la herramienta [kompose](https://kompose.io/). Descargar el binario. Incluirlo al *PATH* o ejecutarlo desde consola, tipo `C:\Users\Sergio-VM\Downloads\kompose.exe`.
  - **Moverse** a la carpeta dedicada para los ficheros: `cd config_for_kubernetes/`.
  - Ejecutar el comando: `kompose convert -f ../docker-compose-resolved.yaml`.
  - **Nota**: Algunos `volumes` no se generan, y habría que hacer los *persistance* manualmente.

8. Incluir los ficheros `.yaml`, generados vía Kompose, en Kubernetes: `kubectl apply -f .`.

9. Verificar que los *pods* y servicios están funcionando:
  - Ver *pods*: `kubectl get pod`. Verificar `Ready 1/1`.
  - Ver servicios: `kubectl get svc`.

10. Testear que los *pods* están funcionando. Kubernetes genera una red no accesible desde el navegador. Por tanto, tenemos que generar una redirección interna de exposición de los puertos de los *servicios* a los que queramos acceder.
  - *IP Forwarding* para probar pgAdmin: `kubectl port-forward svc/pgadmin 5050:5050`
  - *IP Forwarding* para probar la web: `kubectl port-forward svc/app-web 6500:6500`

11. **Borrar todo**. Desde la carpeta de los `.yaml` de configuración de kubernetes (`config_for_kubernetes/`), ejecutar: `kubectl delete -f .`
  - **Nota**: Los *deploys* y servicios se borran *rápidamente*. Sin embargo, propios *pods* tardan un rato en desaparecer como *instancias* de Docker Desktop.