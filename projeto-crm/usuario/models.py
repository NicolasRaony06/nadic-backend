from django.db import models

def is_logged(request):
    if request.user.is_authenticated:
        return True
    return False
