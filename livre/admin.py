from django.contrib import admin
from .models import Livre


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'genre', 'quantite', 'disponible', 'proprietaire', 'date_ajout']
    list_filter = ['genre', 'disponible', 'proprietaire']
    search_fields = ['titre', 'auteur']
    readonly_fields = ['date_ajout']