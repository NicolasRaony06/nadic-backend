from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_produtos, name="view_produtos"),
    path('cadastro/', views.cadastro, name='cadastro_produto'),
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('deletar/<int:id>/', views.deletar_produto, name="deletar_produto"),
    path('comprar/', views.comprar_produtos, name="comprar_produtos"),
    path('dashboard/', views.dashboard_produtos, name="dashboard_produtos"),
]
