"""
WSGI config for tienda_project.
Gunicorn usa este 'application' como punto de entrada.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_project.settings')

application = get_wsgi_application()
