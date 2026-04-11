from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Livre
from .forms import LivreForm, InscriptionForm


# =============================================================================
# VUES D'AUTHENTIFICATION
# =============================================================================

def inscription(request):
    """Vue d'inscription (Sign Up)."""
    if request.user.is_authenticated:
        return redirect('livre_liste')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue, {user.username} ! Votre compte a été créé avec succès.')
            return redirect('livre_liste')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = InscriptionForm()

    return render(request, 'registration/inscription.html', {'form': form})


def connexion(request):
    """Vue de connexion (Login)."""
    if request.user.is_authenticated:
        return redirect('livre_liste')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue, {user.username} !')
            next_url = request.GET.get('next', 'livre_liste')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/connexion.html', {'form': form})


def deconnexion(request):
    """Vue de déconnexion (Logout)."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('livre_liste')


# =============================================================================
# VUES CRUD — LIVRES
# =============================================================================

def livre_liste(request):
    """
    READ — Liste de tous les livres.
    Accessible à tous (connecté ou non).
    Permet la recherche par titre ou auteur.
    """
    query = request.GET.get('q', '')
    livres = Livre.objects.select_related('proprietaire').all()

    if query:
        livres = livres.filter(
            Q(titre__icontains=query) | Q(auteur__icontains=query)
        )

    context = {
        'livres': livres,
        'query': query,
        'total': livres.count(),
    }
    return render(request, 'livres/livre_liste.html', context)


def livre_detail(request, pk):
    """
    READ — Détail d'un livre.
    Accessible à tous (connecté ou non).
    """
    livre = get_object_or_404(Livre, pk=pk)
    est_proprietaire = request.user.is_authenticated and request.user == livre.proprietaire
    return render(request, 'livres/livre_detail.html', {
        'livre': livre,
        'est_proprietaire': est_proprietaire,
    })


@login_required
def livre_creer(request):
    """
    CREATE — Ajouter un nouveau livre.
    L'utilisateur doit être connecté.
    Le livre est automatiquement lié à l'utilisateur connecté.
    """
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.proprietaire = request.user  # Liaison automatique au user connecté
            livre.save()
            messages.success(request, f'Le livre « {livre.titre} » a été ajouté avec succès !')
            return redirect('livre_detail', pk=livre.pk)
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = LivreForm()

    return render(request, 'livres/livre_form.html', {
        'form': form,
        'action': 'Ajouter un livre',
        'btn_label': 'Ajouter',
    })


@login_required
def livre_modifier(request, pk):
    """
    UPDATE — Modifier un livre existant.
    L'utilisateur doit être connecté ET être le propriétaire.
    Retourne 403 Forbidden si l'utilisateur n'est pas le propriétaire.
    """
    livre = get_object_or_404(Livre, pk=pk)

    # Vérification des permissions — SÉCURITÉ
    if request.user != livre.proprietaire:
        raise PermissionDenied  # 403 Forbidden

    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, f'Le livre « {livre.titre} » a été mis à jour avec succès !')
            return redirect('livre_detail', pk=livre.pk)
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = LivreForm(instance=livre)

    return render(request, 'livres/livre_form.html', {
        'form': form,
        'livre': livre,
        'action': 'Modifier le livre',
        'btn_label': 'Enregistrer',
    })


@login_required
def livre_supprimer(request, pk):
    """
    DELETE — Supprimer un livre.
    L'utilisateur doit être connecté ET être le propriétaire.
    Retourne 403 Forbidden si l'utilisateur n'est pas le propriétaire.
    """
    livre = get_object_or_404(Livre, pk=pk)

    # Vérification des permissions — SÉCURITÉ
    if request.user != livre.proprietaire:
        raise PermissionDenied  # 403 Forbidden

    if request.method == 'POST':
        titre = livre.titre
        livre.delete()
        messages.success(request, f'Le livre « {titre} » a été supprimé.')
        return redirect('livre_liste')

    return render(request, 'livres/livre_confirmer_suppression.html', {'livre': livre})