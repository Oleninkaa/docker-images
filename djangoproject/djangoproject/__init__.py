from __future__ import absolute_import, unicode_literals

# Це необхідно, щоб Celery працював разом з Django
from .celery_conf import app as celery_app

__all__ = ('celery_app',)
