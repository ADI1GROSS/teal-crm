try:
    from .celery import app as celery_app
except ImportError:
    celery_app = None  # Celery is optional in local dev / Railway

__all__ = ('celery_app',)
