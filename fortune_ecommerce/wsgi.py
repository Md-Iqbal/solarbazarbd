"""
WSGI config for fortune_ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

# add the hellodjango project path into the sys.path
# sys.path.append('/home/fortunes/solarbazarbd')

# # add the virtualenv site-packages path to the sys.path
# sys.path.append('/home/fortunes/virtualenv/solarbazarbd/Lib/python3.6/site-packages')
# INTERP = '/home/fortunes/virtualenv/solarbazar/bin/python'
# if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortune_ecommerce.settings')

application = get_wsgi_application()




