#!/bin/sh
# Entrypoint del servicio 'web': espera a Postgres, aplica migraciones y arranca Gunicorn.
set -e

echo "Esperando a que Postgres ($DB_HOST:$DB_PORT) este disponible..."
while ! python -c "import socket, os; s=socket.socket(); s.settimeout(1); s.connect((os.environ.get('DB_HOST','db'), int(os.environ.get('DB_PORT','5432'))))" 2>/dev/null; do
  sleep 1
done
echo "Postgres disponible. Aplicando migraciones..."

python manage.py migrate --noinput

echo "Migraciones aplicadas. Arrancando servidor..."
# Ejecuta el comando pasado por docker-compose (gunicorn ...)
exec "$@"
