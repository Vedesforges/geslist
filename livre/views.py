from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LivreForm
from .models import Livre


def utilisateur_est_proprietaire(livre, user):
    return user.is_authenticated and livre.proprietaire == user.username


def utilisateur_peut_gerer_livre(livre, user):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return utilisateur_est_proprietaire(livre, user)


def accueil(request):
    return render(request, "livre/accueil.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Vous avez ete deconnecte avec succes.")
    return redirect("accueil")


@login_required
def livre_liste(request):
    query = request.GET.get("q")
    livres = Livre.objects.all()

    if query:
        livres = livres.filter(titre__icontains=query)

    return render(
        request,
        "livre/livre_list.html",
        {
            "livres": livres,
            "query": query or "",
            "utilisateur_est_admin": request.user.is_superuser or request.user.is_staff,
        },
    )


@login_required
def ajouter_livre(request):
    if request.method == "POST":
        form = LivreForm(request.POST)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.proprietaire = request.user.username
            livre.disponible = livre.quantite > 0
            livre.save()
            messages.success(request, "Le livre a ete ajoute avec succes.")
            return redirect("livre_liste")
    else:
        form = LivreForm()

    return render(request, "livre/livre_form.html", {"form": form, "mode": "ajout"})


@login_required
def supprimer_livre(request, id):
    livre = get_object_or_404(Livre, id=id)

    if not utilisateur_peut_gerer_livre(livre, request.user):
        messages.error(request, "Vous ne pouvez supprimer que les livres que vous avez crees.")
        return redirect("livre_liste")

    if request.method == "POST":
        livre.delete()
        messages.success(request, "Le livre a ete supprime avec succes.")
        return redirect("livre_liste")

    return render(request, "livre/livre_confirm_delete.html", {"livre": livre})


@login_required
def modifier_livre(request, id):
    livre = get_object_or_404(Livre, id=id)

    if not utilisateur_peut_gerer_livre(livre, request.user):
        messages.error(request, "Vous ne pouvez modifier que les livres que vous avez crees.")
        return redirect("livre_liste")

    if request.method == "POST":
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.disponible = livre.quantite > 0
            livre.save()
            messages.success(request, "Le livre a ete modifie avec succes.")
            return redirect("livre_liste")
    else:
        form = LivreForm(instance=livre)

    return render(
        request,
        "livre/livre_form.html",
        {"form": form, "livre": livre, "mode": "modification"},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("livre_liste")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a ete cree et vous etes maintenant connecte.")
            return redirect("livre_liste")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
