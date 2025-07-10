from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar, name="cadastrar_usuario"),
    path('login/', views.login, name="login"),
    
]
