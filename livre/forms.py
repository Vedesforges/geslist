from django import forms

from .models import Livre


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ["titre", "auteur", "genre", "quantite"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre"}),
            "auteur": forms.TextInput(attrs={"class": "form-control", "placeholder": "Auteur"}),
            "genre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Genre"}),
            "quantite": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def clean_quantite(self):
        quantite = self.cleaned_data["quantite"]
        if quantite < 0:
            raise forms.ValidationError("La quantite doit etre positive.")
        return quantite
