"""Snippets Tests"""

# Django imports
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


# App imports
from .models import Language, Snippet
from .forms import SnippetForm

class SnippetsTestCase(TestCase):
    """
    Snippets Test Case Class
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('user1', 'testuser1@test.pl', 'testpass')
        self.user2 = User.objects.create_user('user2', 'testuser2test.pl', 'testpass')
        self.lang1 = Language.objects.create(name='Python', slug='python')
        self.lang2 = Language.objects.create(name='JavaScript', slug='javascript')
        self.snippet1 = Snippet.objects.create(
            user=self.user1,
            name='public snippet1 name',
            description='public snippet1 description',
            snippet="print('public snippet1')",
            language=self.lang1,
            public=True
        )
        self.snippet2 = Snippet.objects.create(
            user=self.user1,
            name='private snippet2 name',
            description='private snippet2 description',
            snippet="print('private snippet2')",
            language=self.lang1,
            public=False
        )
        self.snippet3 = Snippet.objects.create(
            user=self.user1,
            name='public snippet3 name',
            description='public snippet3 description',
            snippet="console.log('public snippet3')",
            language=self.lang2,
            public=True
        )
        self.snippet4 = Snippet.objects.create(
            user=self.user2,
            name='public snippet4 name',
            description='public snippet4 description',
            snippet="print('public snippet4')",
            language=self.lang1,
            public=True
        )
        self.snippet5 = Snippet.objects.create(
            user=self.user2,
            name='public snippet5 name',
            description='public snippet5 description',
            snippet="console.log('public snippet5')",
            language=self.lang2,
            public=True
        )
        self.snippet6 = Snippet.objects.create(
            user=self.user2,
            name='private snippet6 name',
            description='private snippet6 description',
            snippet="print('private snippet6')",
            language=self.lang1,
            public=False
        )

    def test_snippet_model(self):
        snippet3 = Snippet.objects.get(name='public snippet3 name')
        snippet5 = Snippet.objects.get(name='public snippet5 name')

        self.assertEqual(snippet3.user, self.user1)
        self.assertEqual(snippet3.language, self.lang2)
        self.assertEqual(snippet3.snippet, "console.log('public snippet3')")

        self.assertEqual(snippet5.user, self.user2)
        self.assertEqual(snippet5.language, self.lang2)
        self.assertEqual(snippet5.snippet, "console.log('public snippet5')")

    def test_language_model(self):
        self.assertEqual(self.lang1.slug, 'python')
        self.assertEqual(self.lang2.slug, 'javascript')

    def test_index(self):
        response = self.client.get('/')
        context_expected = [
            self.snippet5,
            self.snippet4,
            self.snippet3,
            self.snippet1,
        ]

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['snippet_list'],
            context_expected,
            transform=lambda x: x
        )


    def test_login(self):
        response = self.client.post(
            '/accounts/login/',
            {'username': self.user1.username, 'password': self.user1.password}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/accounts/login/',
            {'username': self.user2.username, 'password': self.user2.password}
        )
        self.assertEqual(response.status_code, 200)


    def test_language(self):
        response = self.client.get('/snippets/language/javascript/')
        context_expected = [
            self.snippet5,
            self.snippet3,
        ]
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['snippet_list'],
            context_expected,
            transform=lambda x: x
        )

        response = self.client.get('/snippets/language/python/')
        context_expected = [
            self.snippet4,
            self.snippet1,
        ]
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['snippet_list'],
            context_expected,
            transform=lambda x: x
        )

        response = self.client.get('/snippets/language/java/')
        self.assertEqual(response.status_code, 404)

    def test_user_snippets(self):
        response = self.client.get('/snippets/user/%s/'%self.user1.username)
        context_expected = [
            self.snippet3,
            self.snippet1,
        ]
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['snippet_list'],
            context_expected,
            transform=lambda x: x
        )

        response = self.client.get('/snippets/user/%s/'%self.user2.username)
        context_expected = [
            self.snippet5,
            self.snippet4,
        ]
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['snippet_list'],
            context_expected,
            transform=lambda x: x
        )


    def test_snippet_add(self):
        response = self.client.post(
            '/accounts/login/',
            {'username': self.user1.username, 'password': self.user1.password}
        )
        snippet = {
            'name': 'test_name',
            'description': 'test_description',
            'snippet': "print('test_snippet')",
            'language': 1,
            'public': True
        }
        form = SnippetForm(data=snippet)
        self.assertTrue(form.is_valid())
        response = self.client.post('/snippets/add/', snippet)
        self.assertEqual(response.status_code, 302)


    def test_snippet(self):
        response = self.client.get('/snippets/snippet/2')
        self.assertEqual(response.context['snippet'].name, 'private snippet2 name')

        response = self.client.get('/snippets/snippet/3')
        self.assertEqual(response.context['snippet'].name, 'public snippet3 name')


    def test_snippet_delete(self):
        response = self.client.post(
            '/accounts/login/',
            {'username': self.user1.username, 'password': self.user1.password}
        )
        response = self.client.get('/snippets/1/delete/')
        self.assertEqual(response.status_code, 302)
