from django.conf import settings
from django.urls import reverse

def get_full_url(viewname, *args, **kwargs):
    """Get URL with FORCE_SCRIPT_NAME prefix"""
    path = reverse(viewname, *args, **kwargs)
    return f"{settings.FORCE_SCRIPT_NAME}{path}"