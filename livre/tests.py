from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Livre


class LivreViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")
        self.other_user = User.objects.create_user(username="bob", password="secret123")
        self.admin_user = User.objects.create_superuser(username="admin", password="secret123", email="admin@example.com")

    def test_authenticated_user_can_create_book(self):
        self.client.login(username="alice", password="secret123")

        response = self.client.post(
            reverse("ajouter_livre"),
            {
                "titre": "Django pour tous",
                "auteur": "A. Auteur",
                "genre": "Technique",
                "quantite": 3,
            },
        )

        self.assertRedirects(response, reverse("livre_liste"))
        livre = Livre.objects.get(titre="Django pour tous")
        self.assertEqual(livre.proprietaire, "alice")
        self.assertTrue(livre.disponible)

    def test_registration_creates_account_and_logs_user_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "charlie",
                "password1": "MonMotdePasse123!",
                "password2": "MonMotdePasse123!",
            },
        )

        self.assertRedirects(response, reverse("livre_liste"))
        self.assertTrue(User.objects.filter(username="charlie").exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_list_page_requires_authentication(self):
        response = self.client.get(reverse("livre_liste"))
        self.assertEqual(response.status_code, 302)

    def test_home_page_displays_auth_links_for_anonymous_user(self):
        response = self.client.get(reverse("accueil"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")
        self.assertContains(response, "Inscription")

    def test_logout_url_logs_user_out(self):
        self.client.login(username="alice", password="secret123")

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("accueil"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_delete_page_confirms_before_removing_book(self):
        self.client.login(username="alice", password="secret123")
        livre = Livre.objects.create(
            titre="A supprimer",
            auteur="Auteur",
            genre="Roman",
            quantite=1,
            disponible=True,
            proprietaire="alice",
        )

        get_response = self.client.get(reverse("supprimer_livre", args=[livre.id]))
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(reverse("supprimer_livre", args=[livre.id]))
        self.assertRedirects(post_response, reverse("livre_liste"))
        self.assertFalse(Livre.objects.filter(id=livre.id).exists())

    def test_user_cannot_edit_book_created_by_another_user(self):
        livre = Livre.objects.create(
            titre="Livre prive",
            auteur="Auteur",
            genre="Roman",
            quantite=2,
            disponible=True,
            proprietaire="alice",
        )
        self.client.login(username="bob", password="secret123")

        response = self.client.post(
            reverse("modifier_livre", args=[livre.id]),
            {
                "titre": "Titre pirate",
                "auteur": "Auteur",
                "genre": "Roman",
                "quantite": 4,
            },
        )

        self.assertRedirects(response, reverse("livre_liste"))
        livre.refresh_from_db()
        self.assertEqual(livre.titre, "Livre prive")

    def test_user_cannot_delete_book_created_by_another_user(self):
        livre = Livre.objects.create(
            titre="Livre protege",
            auteur="Auteur",
            genre="Roman",
            quantite=2,
            disponible=True,
            proprietaire="alice",
        )
        self.client.login(username="bob", password="secret123")

        response = self.client.post(reverse("supprimer_livre", args=[livre.id]))

        self.assertRedirects(response, reverse("livre_liste"))
        self.assertTrue(Livre.objects.filter(id=livre.id).exists())

    def test_admin_can_edit_book_created_by_another_user(self):
        livre = Livre.objects.create(
            titre="Livre admin",
            auteur="Auteur",
            genre="Roman",
            quantite=2,
            disponible=True,
            proprietaire="alice",
        )
        self.client.login(username="admin", password="secret123")

        response = self.client.post(
            reverse("modifier_livre", args=[livre.id]),
            {
                "titre": "Livre admin modifie",
                "auteur": "Auteur",
                "genre": "Roman",
                "quantite": 5,
            },
        )

        self.assertRedirects(response, reverse("livre_liste"))
        livre.refresh_from_db()
        self.assertEqual(livre.titre, "Livre admin modifie")

    def test_admin_can_delete_book_created_by_another_user(self):
        livre = Livre.objects.create(
            titre="Livre admin suppression",
            auteur="Auteur",
            genre="Roman",
            quantite=2,
            disponible=True,
            proprietaire="alice",
        )
        self.client.login(username="admin", password="secret123")

        response = self.client.post(reverse("supprimer_livre", args=[livre.id]))

        self.assertRedirects(response, reverse("livre_liste"))
        self.assertFalse(Livre.objects.filter(id=livre.id).exists())
