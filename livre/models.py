from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    quantite = models.IntegerField()
    disponible = models.BooleanField(default=True)
    proprietaire = models.CharField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.titre