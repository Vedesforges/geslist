from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Livre


class LivreForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier un livre.
    Le champ 'proprietaire' est exclu car il est assigné automatiquement dans la vue.
    """
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'description', 'genre', 'quantite', 'disponible']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Le Petit Prince',
            }),
            'auteur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Antoine de Saint-Exupéry',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le livre en quelques lignes...',
            }),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titre': 'Titre du livre',
            'auteur': 'Auteur',
            'description': 'Description',
            'genre': 'Genre',
            'quantite': 'Quantité en stock',
            'disponible': 'Disponible à l\'emprunt',
        }


class InscriptionForm(UserCreationForm):
    """
    Formulaire d'inscription étendu avec le champ email.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer Bootstrap aux champs existants
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user