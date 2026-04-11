from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Livre(models.Model):
    """
    Modèle représentant un livre dans la bibliothèque.
    Contient 5 champs métier + un champ propriétaire (ForeignKey vers User).
    """
    GENRE_CHOICES = [
        ('roman', 'Roman'),
        ('science', 'Science'),
        ('histoire', 'Histoire'),
        ('biographie', 'Biographie'),
        ('philosophie', 'Philosophie'),
        ('informatique', 'Informatique'),
        ('art', 'Art & Culture'),
        ('autre', 'Autre'),
    ]

    # Champs métier (5 champs minimum requis)
    titre = models.CharField(max_length=200, verbose_name="Titre")
    auteur = models.CharField(max_length=150, verbose_name="Auteur")
    description = models.TextField(verbose_name="Description")
    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        default='autre',
        verbose_name="Genre"
    )
    quantite = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    isbn = models.CharField(max_length=13, blank=True, null=True, verbose_name="ISBN")  # Nouveau champ ajouté

    # Champ propriétaire (ForeignKey vers User — requis par le cahier des charges)
    proprietaire = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='livres',
        verbose_name="Propriétaire"
    )

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Livre"
        verbose_name_plural = "Livres"

    def __str__(self):
        return f"{self.titre} — {self.auteur}"

    def get_absolute_url(self):
        return reverse('livre_detail', kwargs={'pk': self.pk})