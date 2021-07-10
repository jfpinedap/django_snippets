"""Snippet Views"""

# Django imports
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

# App imports
from .models import Language, Snippet
from .owner import (
    OwnerDeleteView,
    OwnerDetailView,
    OwnerListView,
)
from .forms import SnippetForm
from .tasks import sendEmail


class IndexView(OwnerListView):
    model = Snippet
    template_name = 'index.html'

    def get(self, request) :
        snippet_list = Snippet.objects.filter(
            public=True
        ).order_by('-created')

        context = {'snippet_list' : snippet_list}
        return render(request, self.template_name, context)


class SnippetByLangView(OwnerListView):
    model = Snippet
    template_name = 'index.html'

    def get(self, request, lang_slug):
        _language = get_object_or_404(Language, slug=lang_slug)
        snippet_list = Snippet.objects.filter(
            public=True,
            language__slug = _language.slug
        ).order_by('-created')

        context = {'snippet_list' : snippet_list}
        return  render(request, self.template_name, context)


class SnippetByUserView(OwnerListView):
    model = Snippet
    template_name = 'snippets/user_snippets.html'

    def get(self, request, username):
        _user = get_object_or_404(User, username=username)

        query = Q(user=_user)
        if not request.user.is_authenticated or request.user != _user:
            query.add(Q(public=True), Q.AND)

        snippet_list = Snippet.objects.filter(query).order_by('-created')

        context = {'snippet_list' : snippet_list}
        return render(request, self.template_name, context)


class SnippetDetailView(OwnerDetailView):
    model = Snippet
    template_name = "snippets/snippet.html"

    def get(self, request, pk) :
        _snippet = get_object_or_404(Snippet, id=pk)
        context = { 'snippet' : _snippet}
        return render(request, self.template_name, context)


class SnippetAddView(LoginRequiredMixin, View):
    template_name = 'snippets/snippet_add.html'
    success_url = reverse_lazy('snipets:index')

    def get(self, request):
        form = SnippetForm()
        context = {'form': form, 'create': True}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SnippetForm(request.POST)

        if not form.is_valid():
            context = {'form': form, 'create': True}
            return render(request, self.template_name, context)

        # Add user to the model before saving
        _snippet = form.save(commit=False)
        _snippet.user = self.request.user
        _snippet.save()

        # send confirmation email
        sendEmail.delay(
            subject=_snippet.name,
            body=_snippet.description,
            email=_snippet.user.email
        )
        return redirect(self.success_url)


class SnippetEditView(LoginRequiredMixin, View):
    template_name = 'snippets/snippet_add.html'
    success_url = reverse_lazy('snipets:index')

    def get(self, request, pk):
        _snippet = get_object_or_404(Snippet, id=pk, user=self.request.user)
        form = SnippetForm(instance=_snippet)
        context = {'form': form, 'create': False}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        _snippet = get_object_or_404(Snippet, id=pk, user=self.request.user)
        form = SnippetForm(request.POST, request.FILES or None, instance=_snippet)

        if not form.is_valid():
            context = {'form': form, 'create': False}
            return render(request, self.template_name, context)

        _snippet = form.save(commit=False)
        _snippet.save()

        return redirect(self.success_url)


class SnippetDeleteView(OwnerDeleteView):
    model = Snippet
