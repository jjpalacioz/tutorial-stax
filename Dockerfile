FROM python:3.12-slim

# Evita que Python genere archivos .pyc y activa salida sin buffer (mejor para logs en Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias primero (aprovecha la cache de Docker)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Entrypoint: espera a la DB y aplica migraciones antes de arrancar
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Gunicorn se ejecuta segun el 'command' definido en docker-compose.yml
EXPOSE 8000
