# Aplicación de Votación (Dubstep vs. Raw) con Docker y CI/CD

Este es un proyecto de aplicación web full-stack diseñado para demostrar una arquitectura de microservicios moderna utilizando Docker. La aplicación permite a los usuarios votar en tiempo real entre dos géneros de música ("Dubstep" y "Raw") y ver los resultados en una página de estadísticas separada.

El proyecto está completamente "dockerizado" y configurado para un despliegue automático (CI/CD) en un servidor propio (self-hosted) mediante GitHub Actions.

---

## 🚀 Tecnologías Utilizadas

* **Backend:** Python con el micro-framework Flask.
* **Frontend:** HTML5, Tailwind CSS (para el diseño) y JavaScript (con `fetch` para la interactividad).
* **Base de Datos (Caché):** Redis (para el conteo de votos en tiempo real).
* **Base de Datos (Persistente):** PostgreSQL (configurado, listo para almacenar los resultados a largo plazo).
* **Servidor / Reverse Proxy:** Nginx.
* **Contenedores y Orquestación:** Docker y Docker Compose.
* **CI/CD (Automatización):** GitHub Actions con un Self-Hosted Runner.

---

## 🏗️ Arquitectura del Sistema

El proyecto se ejecuta como un conjunto de servicios interconectados definidos en `docker-compose.yml`:

* **Usuario:** El usuario accede al proyecto a través de `http://localhost:8080`.
* **Nginx (`nginx`):** Este contenedor actúa como el reverse proxy. Recibe la petición del usuario en el puerto 8080 y la reenvía al servicio de la aplicación Flask.
* **Aplicación Flask (`web-app`):** Este es el cerebro de la aplicación.
    * Sirve las páginas `index.html` (para votar) y `results.html` (para ver estadísticas).
    * Proporciona una API (`/vote` y `/results`).
    * Se comunica con Redis para registrar votos y leer los conteos.
* **Caché (`redis`):** Almacena los contadores de "dubstep" y "raw" en memoria para un acceso de lectura/escritura ultra-rápido.
* **Base de Datos (`postgres`):** El servicio de base de datos persistente. Aunque en la lógica actual solo usamos Redis, Postgres está configurado y conectado, listo para que la aplicación guarde los resultados permanentemente.

---

## 📁 Estructura de Archivos

```plaintext
.
├── .github/workflows/deploy.yml  # Workflow de CI/CD para el despliegue automático
├── app/                          # Código fuente de la aplicación Flask
│   ├── app.py                    # Lógica del backend (Flask)
│   ├── index.html                # Página principal de votación
│   ├── results.html              # Página de estadísticas con gráfico
│   ├── Dockerfile                # Instrucciones para construir la imagen de Flask
│   └── requirements.txt          # Dependencias de Python
├── nginx/                        # Configuración del reverse proxy Nginx
│   ├── nginx.conf                # Reglas de Nginx (proxy_pass)
│   └── Dockerfile                # Instrucciones para construir la imagen de Nginx
├── .env                          # (Local - Ignorado por Git) Variables de entorno
├── docker-compose.yml            # Orquestador principal de todos los servicios
└── README.md                     # Este archivo
```

---

## 🚀 Cómo Ejecutar (Desarrollo Local)

Para levantar todo el sistema en tu máquina local:

1.  **Clona el repositorio:**

    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Crea el archivo `.env`:**
    Crea un archivo llamado `.env` en la raíz del proyecto y copia el siguiente contenido. Este archivo le dará las contraseñas y nombres a los servicios de Docker Compose.

    ```ini
    # Credenciales de PostgreSQL
    POSTGRES_DB=pgdb
    POSTGRES_USER=pguser
    POSTGRES_PASSWORD=pg123
    POSTGRES_HOST=postgres
    
    # Configuración de Redis
    REDIS_HOST=redis
    REDIS_PORT=6379
    ```

3.  **Construye y levanta los servicios:**
    Este comando construirá las imágenes personalizadas de `web-app` y `nginx` y luego iniciará todos los contenedores.

    ```bash
    docker compose up --build
    ```
    *(Si quieres que se ejecute en segundo plano, añade `-d` al final).*

4.  **Accede a la aplicación:**
    Abre tu navegador y ve a: `http://localhost:8080`

---

## 🤖 Despliegue Automático (CI/CD)

Este repositorio está configurado con un flujo de trabajo (`.github/workflows/deploy.yml`) que automatiza el despliegue en un servidor (runner "self-hosted") cada vez que se hace un `push` a la rama `main`.

**Lo que hace el workflow:**

* **Activación:** Se dispara con un `push` a `main`.
* **Runner:** Espera a que un runner con las etiquetas `self-hosted` y `linux` esté disponible.
* **Checkout:** Descarga el código fuente más reciente.
* **Crear .env:** No usa el archivo `.env` local. En su lugar, crea uno nuevo usando los Secretos del Repositorio (ej. `${{ secrets.POSTGRES_PASSWORD }}`) configurados en GitHub.
* **Parar y Limpiar:** Ejecuta `docker compose down -v` para detener y eliminar contenedores y volúmenes antiguos.
* **Construir:** Ejecuta `docker compose build` para crear las nuevas imágenes con los cambios.
* **Levantar:** Ejecuta `docker compose up -d` para iniciar los servicios actualizados.
* **Verificar:** Espera 10 segundos y ejecuta un `curl` a `localhost:8080` para asegurarse de que la aplicación ha respondido correctamente.