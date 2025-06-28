from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro_produto'),
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
]
