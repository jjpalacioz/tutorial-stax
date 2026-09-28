import socket

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def comprar(request):
    """
    Endpoint de compras: /api/v1/comprar/

    Devuelve un JSON de confirmacion. Sirve como evidencia de que Nginx
    esta enrutando el trafico del puerto 80 hacia Django/Gunicorn.
    El campo 'servido_por' muestra el hostname del contenedor 'web',
    demostrando que la peticion paso por el proxy inverso.
    """
    if request.method == 'POST':
        producto = request.data.get('producto', 'producto-demo')
        cantidad = request.data.get('cantidad', 1)
        mensaje = f"Compra registrada: {cantidad} x {producto}"
    else:
        mensaje = "Endpoint de compras operativo. Envie un POST para registrar una compra."

    return Response({
        'ok': True,
        'servicio': 'API de Compras v1',
        'mensaje': mensaje,
        'ruta': '/api/v1/comprar/',
        'servido_por_contenedor': socket.gethostname(),
        'nota': 'Si ves esto SIN el puerto :8000 en la URL, Nginx enruta correctamente por el puerto 80.',
    })
