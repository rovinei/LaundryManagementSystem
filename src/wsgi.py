"""
WSGI config for laundry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

project_path = "/Users/keen/Desktop/Vinei/Projects/Django/LaundryManagement"
sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.settings")

application = get_wsgi_application()

