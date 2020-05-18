"""
WSGI config for bookstore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import sys
import os
# from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

sys.path.append('/home/ubuntu/django/bookstore')
sys.path.append('/home/ubuntu/django/bookstore/bookstore')
application = get_wsgi_application()
# application = DjangoWhiteNoise(application)
