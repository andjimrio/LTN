"""
WSGI config for LTNews project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/home/andjimrio/LTN'  # aquí utiliza tu propio usuario, sin los simbolos < y >
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LTNews.settings")

application = get_wsgi_application()


