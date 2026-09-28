# Tutorial 05: El Escudo Arquitectónico

Arquitectura de producción de tres capas: **Nginx (Proxy Inverso)** + **Gunicorn (WSGI)** + **Django** + **PostgreSQL**, dockerizada y lista para desplegar en AWS EC2. Es la base para implementar el *Strangler Pattern*.

```
Internet ──▶ [ Nginx :80 ] ──▶ [ web: Gunicorn :8000 (Django) ] ──▶ [ db: Postgres :5432 ]
             (única cara            (aislado, sin puertos              (aislado)
              a internet)            expuestos al host)
```

## Estructura del proyecto

```
.
├── docker-compose.yml        # Orquesta nginx + web + db
├── Dockerfile                # Imagen del servicio web (Django + Gunicorn)
├── entrypoint.sh             # Espera a Postgres y aplica migraciones antes de arrancar
├── requirements.txt          # Incluye gunicorn
├── manage.py
├── nginx/
│   └── nginx.conf            # Proxy inverso: puerto 80 -> upstream django_backend (web:8000)
├── tienda_project/           # Proyecto Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── compras/                  # App con el endpoint /api/v1/comprar/
    ├── urls.py
    ├── views.py
    └── models.py
```

## El endpoint de evidencia

`GET/POST http://<IP-EC2>/api/v1/comprar/` devuelve un JSON de confirmación. Sirve para la **captura de enrutamiento**: si responde **sin** el puerto `:8000` en la URL, Nginx está enrutando por el puerto 80.

---

## Despliegue en AWS EC2

### 1. Subir a GitHub (desde tu máquina local)
```bash
git add .
git commit -m "Tutorial 05: Nginx + Gunicorn + Django dockerizado"
git push origin main
```

### 2. Entrar por SSH a la instancia EC2 y desplegar
```bash
# 1. Entre a la carpeta de su proyecto en EC2
cd mi-proyecto-django

# 2. Descargue los nuevos cambios
git pull origin main

# 3. Reconstruya y levante la nueva arquitectura
docker compose up -d --build

# 4. Verifique que los TRES contenedores esten corriendo (db, web, nginx)
docker ps
```

### 3. Configurar el Security Group (Firewall) en AWS
1. Consola AWS → **EC2 → Security Groups**.
2. Seleccione el grupo asociado a su instancia.
3. **Edit inbound rules → Add rule**.
4. **Type:** HTTP → **Port range:** 80 → **Source:** 0.0.0.0/0.
5. **Save rules**.

> Nota: NO abra el puerto 8000. Django debe quedar aislado; ese aislamiento es justamente la Evidencia 2.

---

## Entrega: las 3 capturas

Estas capturas debes tomarlas **tú** desde tu entorno real (navegador, terminal local y consola de AWS). Aquí tienes exactamente qué hacer para cada una:

### 📸 Captura 1 — Evidencia de Enrutamiento (navegador)
1. Abre en tu navegador: `http://<IP-EC2>/api/v1/comprar/` (reemplaza `<IP-EC2>` por la IP pública de tu instancia).
2. Debe verse el JSON de respuesta de la API.
3. **Captura la pantalla asegurándote de que la barra de direcciones sea visible y NO tenga `:8000`.**
   - ✅ Correcto: `http://54.x.x.x/api/v1/comprar/`
   - ❌ Incorrecto: `http://54.x.x.x:8000/api/v1/comprar/`

### 📸 Captura 2 — Evidencia de Aislamiento (terminal local)
1. Desde tu **terminal local** (no la de EC2), intenta acceder al puerto 8000:
   ```bash
   curl -v --max-time 10 http://<IP-EC2>:8000
   ```
   O ábrelo en el navegador: `http://<IP-EC2>:8000`
2. **Debe fallar con timeout** (se queda colgado y expira). Eso prueba que Django está aislado.
3. Captura la pantalla mostrando el timeout / la conexión rechazada.

### 📸 Captura 3 — Evidencia de Orquestación (terminal AWS)
1. En la terminal SSH de tu EC2, ejecuta:
   ```bash
   docker ps
   ```
2. Deben verse los **tres contenedores** (`nginx`, `web`, `db`) en estado **`Up`**.
3. Captura la pantalla completa mostrando la salida.

### Dónde poner las capturas
Cuando las tengas, súbelas a la plataforma del curso. Si quieres, colócalas en una carpeta `docs/capturas/` de este repo y podemos armar un informe de entrega con las imágenes incrustadas.

---

## Verificación local (opcional, antes de EC2)
Si tienes Docker en tu máquina, puedes probar todo localmente:
```bash
docker compose up -d --build
docker ps                               # deben aparecer los 3 contenedores
curl http://localhost/api/v1/comprar/   # debe responder el JSON (puerto 80, sin :8000)
curl --max-time 5 http://localhost:8000 # debe fallar/timeout (Django aislado)
docker compose down                     # para apagar
```
