from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('livres/', views.livre_liste, name='livre_liste'),
    path('ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('supprimer/<int:id>/', views.supprimer_livre, name='supprimer_livre'),
    path('modifier/<int:id>/', views.modifier_livre, name='modifier_livre'),
    path('register/', views.register, name='register'),
]
